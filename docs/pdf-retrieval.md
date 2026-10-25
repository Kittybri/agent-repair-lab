# Case study: a PDF failed before text extraction

## Problem

On October 22, 2026, a user submitted the same study file to two Discord character bots through `!tedtalk`. Wanderer generated a lecture. Scaramouche replied that he could not retrieve the file. The task was to restore the behavior with a narrow change.

## Evidence and diagnosis

The investigation followed the actual running service rather than assuming an older local checkout matched production. A read-only probe used Scaramouche's existing Discord access to retrieve the recent attachment. No message was posted by the probe.

| Observation | Interpretation |
| --- | --- |
| Cached attachment read returned HTTP 415 | Retrieval failed before the PDF parser ran. |
| Original attachment read returned 1,697,299 bytes | The original file was accessible to the same bot. |
| Neither configured PDF parser was installed in Scaramouche's environment | Fixing retrieval alone would expose a second failure. |
| Wanderer's environment had PyPDF2 3.0.1 | An existing fallback supported a narrow dependency fix. |

The uploaded PDF and its text are not included in this repository.

## Change and tradeoffs

The retrieval change replaced a forced cached read with an original-first read and one cached fallback for `discord.HTTPException`. Each attempt retained a 30-second timeout. Declared and downloaded sizes remained limited to 20 MB. PyPDF2 3.0.1 was installed and added to the deployed dependency file.

The download change added four source lines and removed one. It preserved the existing parser fallback and command behavior. A fallback can make total waiting time approach two per-attempt timeouts. A whole-operation deadline and streaming size cap would be sensible follow-up work, but were outside this narrow fix.

## Verification

The same 25-page PDF downloaded through the original endpoint. The existing fallback extracted the configured 8,000-character material budget. Six focused regression tests checked original-first access, cached fallback, both endpoints failing, size checks before and after download, and timeout propagation. The modified source compiled, and the restarted service logged a successful Discord connection and online state.

These observations verify retrieval and text extraction. They do not establish complete document comprehension, lecture factual accuracy, speech quality, or long-term uptime. The probe did not trigger another full lecture.

## Reproduce safely

The [attachment task](../tasks/attachment/TASK.md) replaces Discord and the private PDF with fake attachment objects. It includes an intentionally broken starter and a reference repair. Its grader extends the regression cases with a boundary-sized file and a timeout on the fallback URL.

## Engineering lesson

Diagnose by pipeline stage: download, parsing, generation, then delivery. One successful download does not prove parsing is available. A small patch still needs dependency verification and checks that preserve existing failure behavior.
