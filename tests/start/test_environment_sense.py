from shorter.start.environment import (
    DELAY_DEF,
    DELAY_MAX,
    DELAY_MIN,
    DELAY_STP,
)


def test_delay_sense():
    assert DELAY_MIN <= DELAY_MAX
    assert DELAY_STP <= DELAY_MAX

    assert DELAY_DEF >= DELAY_MIN
    assert DELAY_DEF <= DELAY_MAX

    assert DELAY_DEF % DELAY_STP == 0
