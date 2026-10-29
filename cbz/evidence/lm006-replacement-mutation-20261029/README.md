# LM006 Git replacement mutation correction

At head 68cf855bcc953cad6c4a7ac8f04d201d2ccf7949, run 40948228286 observed 20 passes and one failing mutation-control test in both modes. The replacement mutant set GIT_NO_REPLACE_OBJECTS to the string '0'. Git interprets the variable's presence as enabling the no-replacement behavior, so the supposed mutant remained protected. This successor removes the variable from the subprocess environment in the mutant. The original test and the production guard remain unchanged. This records a harness correction, not evidence that the corrected mutant has yet been killed.

Decision 2026-10-29 20:29:31 UTC: retain both original failure excerpts and all three source mutations; run the corrected test in both modes on the new source. No numerical code or bounds change.
