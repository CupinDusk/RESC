Protocol inputs and all case populations remain unchanged.

1. **attempt-001, compile failure, preserved.** Actual Yosys0.70 synthesis
   succeeded and emitted `#include <cxxrtl/cxxrtl.h>`. The first compiler command
   supplied only Yosys `share/include` as requested by the environment hint;
   Zig reported `fatal error: 'cxxrtl/cxxrtl.h' file not found`. The portable
   runner now also supplies `share/include/backends/cxxrtl/runtime`, where
   that header actually resides. Both include roots are retained. No RTL,
   vector, guard, observation, or graph decision was changed.

Additional source detail, visible before execution: after each valid capture,
the driver changes external `cfgn` to `N+777` to check that the countdown uses
the reset-latched count. This is neither a new private-count case nor an
auditor input. A repeated start while busy is additionally diagnosed as
reason8 by RTL; it is outside the four declared invalid-control families.
