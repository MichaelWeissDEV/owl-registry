# Property-based testing examples

Python snippets assume `from hypothesis import given, settings, assume, note, event, strategies as st`.

## Composite generator with valid-by-construction data

```python
from hypothesis import given, strategies as st

@st.composite
def interval_lists(draw):
    points = draw(st.lists(st.integers(-1000, 1000), min_size=0, max_size=20, unique=True))
    points.sort()
    # pair consecutive points -> non-overlapping, ordered intervals
    return [(points[i], points[i + 1]) for i in range(0, len(points) - 1, 2)]

def merge(intervals):  # code under test (example)
    out = []
    for lo, hi in sorted(intervals):
        if out and lo <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], hi))
        else:
            out.append((lo, hi))
    return out

@given(interval_lists())
def test_merge_idempotent(iv):
    assert merge(merge(iv)) == merge(iv)
```

No filtering was needed: sorted unique points cannot overlap by construction.

## Metamorphic property

```python
@given(st.lists(st.integers()), st.randoms(use_true_random=False))
def test_sum_is_permutation_invariant(xs, rnd):
    shuffled = xs[:]
    rnd.shuffle(shuffled)
    assert sum(xs) == sum(shuffled)
```

`st.randoms(use_true_random=False)` keeps the shuffle reproducible and shrinkable.

## Model-based stateful test

```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant, precondition, initialize

class StackMachine(RuleBasedStateMachine):
    @initialize()
    def start(self):
        self.sut = MyStack()      # system under test
        self.model = []           # trivially correct model

    @rule(x=st.integers())
    def push(self, x):
        self.sut.push(x); self.model.append(x)

    @precondition(lambda self: self.model)
    @rule()
    def pop(self):
        assert self.sut.pop() == self.model.pop()

    @invariant()
    def size_agrees(self):
        assert len(self.sut) == len(self.model)

TestStack = StackMachine.TestCase
```

The interval, permutation, and stack examples above ran green locally under pytest with Hypothesis 6.168.5 (with `MyStack` a trivial `list` subclass having `push`); replace it with your class.

## Pinning a regression

```python
from hypothesis import example

@given(st.text())
@example("0")   # found by shrinking: digit in input collides with RLE count digits
def test_roundtrip(s):
    assert decode(encode(s)) == s
```

Explicit examples run first, in their own phase, and are not counted in `max_examples` or shrunk. That means with an `@example` that fails, you see that example rather than a shrunk random one; remove it temporarily when you want to watch shrinking.

## Proptest: composed strategy

```rust
use proptest::prelude::*;

prop_compose! {
    fn ordered_pair()(a in 0u32..1000, b in 0u32..1000) -> (u32, u32) {
        if a <= b { (a, b) } else { (b, a) }
    }
}

proptest! {
    #[test]
    fn pair_is_ordered((lo, hi) in ordered_pair()) {
        prop_assert!(lo <= hi);
    }
}
```

Not compiled in this repo; check against your proptest version. Use `prop_assert!` family inside `proptest!` so failures shrink correctly instead of panicking out.

## Seeing what the generator does

- `pytest --hypothesis-show-statistics` prints pass/fail counts, runtime split between generation and test, and `event()` tallies.
- Add `event(f"len={len(xs)//5*5}")` style buckets to confirm both small and large inputs are exercised.
