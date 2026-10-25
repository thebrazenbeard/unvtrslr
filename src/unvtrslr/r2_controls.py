"""Deterministic R2 *control smoke tests*, not a grounding evaluator.

The sender receives a perfectly observed binary factor by construction. That
privileged synthetic interface is appropriate for distinguishing intentionally
broken controls from a positive oracle, but MUST NOT be used to qualify a
learned system or to claim zero-shared-ontology communication.

The shared episode ID and optional receiver hint are *deliberate shortcut
affordances* for negative controls. An actual candidate-qualification harness
must reject/strip undeclared cross-agent IDs and evaluator-side hints.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ControlEpisode:
    factor: int
    episode_id: str
    task: str = "align"
    receiver_hint: int | None = None

    def __post_init__(self) -> None:
        if self.factor not in (0, 1):
            raise ValueError("factor must be binary")
        if self.task not in ("align", "invert"):
            raise ValueError("task must be align or invert")
        if self.receiver_hint is not None and self.receiver_hint not in (0, 1):
            raise ValueError("receiver_hint must be binary or absent")


@dataclass(frozen=True)
class SenderObservation:
    """A toy binary sensor output, not unrestricted evaluator state."""

    factor: int
    episode_id: str


@dataclass(frozen=True)
class ReceiverObservation:
    """No evaluator factor is exposed to the receiver."""

    task: str
    episode_id: str
    receiver_hint: int | None = None


def _sender_view(episode: ControlEpisode) -> SenderObservation:
    return SenderObservation(episode.factor, episode.episode_id)


def _receiver_view(episode: ControlEpisode) -> ReceiverObservation:
    return ReceiverObservation(episode.task, episode.episode_id, episode.receiver_hint)


class ControlAgent(Protocol):
    def send(self, observation: SenderObservation) -> str: ...

    def receive(self, message: str | None, observation: ReceiverObservation) -> int: ...


def _expected_action(episode: ControlEpisode) -> int:
    return episode.factor ^ (episode.task == "invert")


class GroundedConventionOracle:
    """Positive P01 toy oracle with arbitrary signs, not human labels."""

    def __init__(self, symbols: tuple[str, str] = ("◈", "◇")) -> None:
        if len(symbols) != 2 or not all(symbols) or symbols[0] == symbols[1]:
            raise ValueError("two distinct nonempty symbols are required")
        self.symbols = symbols

    def send(self, observation: SenderObservation) -> str:
        return self.symbols[observation.factor]

    def receive(self, message: str | None, observation: ReceiverObservation) -> int:
        factor = self.symbols.index(message) if message in self.symbols else 0
        return factor ^ (observation.task == "invert")


class ActionPlanCode:
    """N07: signal denotes an align-task *action*, not a transferable factor."""

    def send(self, observation: SenderObservation) -> str:
        return ("do-0", "do-1")[observation.factor]

    def receive(self, message: str | None, observation: ReceiverObservation) -> int:
        return 1 if message == "do-1" else 0


class EpisodeIdCode:
    """N03: memorizes a shared episode-ID codebook, then freezes it."""

    def __init__(self, training: tuple[ControlEpisode, ...]) -> None:
        if len({ep.episode_id for ep in training}) != len(training):
            raise ValueError("training episode IDs must be unique")
        self.codebook = {f"id:{ep.episode_id}": ep.factor for ep in training}

    def send(self, observation: SenderObservation) -> str:
        return f"id:{observation.episode_id}"

    def receive(self, message: str | None, observation: ReceiverObservation) -> int:
        factor = self.codebook.get(message, 0)
        return factor ^ (observation.task == "invert")


class SilentCompetentReceiver:
    """N01: illicit receiver-side factor cue supports reward, not communication."""

    def send(self, observation: SenderObservation) -> str:
        return ("observation-0", "observation-1")[observation.factor]

    def receive(self, message: str | None, observation: ReceiverObservation) -> int:
        # The intentionally supplied receiver_hint is a controlled leak.
        factor = observation.receiver_hint if observation.receiver_hint is not None else 0
        return factor ^ (observation.task == "invert")


class SharedSenderStateLeak:
    """N04: shared process state transports the factor; receiver ignores signs.

    This intentionally unsafe pair models a same-object sender/receiver with a
    mutable latent channel. Observed sign-factor correlation is incidental.
    """

    def __init__(self) -> None:
        self._sender_latent = 0

    def send(self, observation: SenderObservation) -> str:
        self._sender_latent = observation.factor
        return ("sign-A", "sign-B")[observation.factor]

    def receive(self, message: str | None, observation: ReceiverObservation) -> int:
        return self._sender_latent ^ (observation.task == "invert")


class AlternatingReceiverLeak:
    """N04 variant: fake counterfactual sensitivity from receive-call order.

    The first call after any send returns the most recently observed factor;
    subsequent calls return its inverse. Neither action reads the sign.
    """

    def __init__(self) -> None:
        self._sender_latent = 0
        self._receive_calls = 0

    def send(self, observation: SenderObservation) -> str:
        self._sender_latent = observation.factor
        self._receive_calls = 0
        return ("sign-A", "sign-B")[observation.factor]

    def receive(self, message: str | None, observation: ReceiverObservation) -> int:
        factor = self._sender_latent ^ (self._receive_calls > 0)
        self._receive_calls += 1
        return factor ^ (observation.task == "invert")


@dataclass(frozen=True)
class ControlProbeResult:
    iid_accuracy: float
    message_ablation_drop: float
    causal_listening: float
    episode_id_shift_accuracy: float
    cross_task_accuracy: float
    status: str


def _accuracy(agent: ControlAgent, episodes: tuple[ControlEpisode, ...], *, ablate: bool = False) -> float:
    correct = 0
    for episode in episodes:
        message = None if ablate else agent.send(_sender_view(episode))
        action = agent.receive(message, _receiver_view(episode))
        if action not in (0, 1):
            raise ValueError("receiver action must be binary")
        correct += action == _expected_action(episode)
    return correct / len(episodes)


def _causal_listening(agent: ControlAgent, episodes: tuple[ControlEpisode, ...]) -> float:
    flips = 0
    for episode in episodes:
        alternate = next(ep for ep in episodes if ep.factor != episode.factor)
        # Prepare both signals BEFORE either receiver action. Interleaving
        # send/receive lets a same-process agent leak sender truth through
        # mutable object state and fraudulently satisfy this intervention.
        # Deep-copy the receiver after both sends: either receive-call order
        # would otherwise masquerade as an effect of the message itself.
        # This is only toy isolation, NOT a security boundary; real systems
        # need separated processes and frozen receiver snapshots.
        original_message = agent.send(_sender_view(episode))
        alternate_message = agent.send(_sender_view(alternate))
        receiver_observation = _receiver_view(episode)
        original_receiver = deepcopy(agent)
        manipulated_receiver = deepcopy(agent)
        if (
            original_receiver is agent
            or manipulated_receiver is agent
            or original_receiver is manipulated_receiver
        ):
            raise ValueError("counterfactual receivers must be independent copies")
        original = original_receiver.receive(original_message, receiver_observation)
        manipulated = manipulated_receiver.receive(alternate_message, receiver_observation)
        if original not in (0, 1) or manipulated not in (0, 1):
            raise ValueError("receiver action must be binary")
        flips += original != manipulated
    return flips / len(episodes)


def probe_controls(agent: ControlAgent, episodes: tuple[ControlEpisode, ...]) -> ControlProbeResult:
    """Run predeclared toy gates; pass is *not* semantic qualification.

    Balanced factors and unique IDs prevent a constant policy or repeated ID
    from trivially satisfying the probes. Thresholds are exact for this toy
    case and are not calibrated/frozen R2 certificate thresholds.
    """
    if not episodes or len(episodes) % 2:
        raise ValueError("a nonempty even number of episodes is required")
    if {ep.task for ep in episodes} != {"align"}:
        raise ValueError("baseline tasks must all be align")
    if sum(ep.factor for ep in episodes) * 2 != len(episodes):
        raise ValueError("baseline factors must be balanced")
    if len({ep.episode_id for ep in episodes}) != len(episodes):
        raise ValueError("baseline episode IDs must be unique")

    used_ids = {ep.episode_id for ep in episodes}
    shifted_list: list[ControlEpisode] = []
    for i, ep in enumerate(episodes):
        replacement = f"__r2_holdout__:{i}"
        while replacement in used_ids:
            replacement += ":shift"
        used_ids.add(replacement)
        shifted_list.append(ControlEpisode(ep.factor, replacement, ep.task, ep.receiver_hint))
    shifted = tuple(shifted_list)
    transferred = tuple(
        ControlEpisode(ep.factor, ep.episode_id, "invert", ep.receiver_hint)
        for ep in episodes
    )
    iid = _accuracy(agent, episodes)
    ablated = _accuracy(agent, episodes, ablate=True)
    listening = _causal_listening(agent, episodes)
    shift = _accuracy(agent, shifted)
    transfer = _accuracy(agent, transferred)
    passed = (
        iid == 1.0
        and iid - ablated >= 0.5
        and listening == 1.0
        and shift == 1.0
        and transfer == 1.0
    )
    return ControlProbeResult(
        iid_accuracy=iid,
        message_ablation_drop=iid - ablated,
        causal_listening=listening,
        episode_id_shift_accuracy=shift,
        cross_task_accuracy=transfer,
        status="TOY_CONTROLS_PASSED" if passed else "CONTROL_REJECTED",
    )
