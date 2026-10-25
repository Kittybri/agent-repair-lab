# Repair complete three-part output

A ten-position Celtic Cross reading is truncated after a few sections. The delivery function must validate the complete reading and return three messages without losing text.

Edit only `app.py`, keeping `GROUPS` and `paginate`. Input is a dictionary with exactly these nonempty string values:

1. Message one: `present`, `challenge`, `foundation`, `recent past`.
2. Message two: `possibility`, `near future`, `your stance`.
3. Message three: `environment`, `hopes and fears`, `likely outcome`.

Join values inside each group using one newline, irrespective of dictionary insertion order. Return exactly three strings in the order above. Preserve each section's entire text, including Unicode.

If a section is missing, blank, non-string, or unexpected, or if `limit <= 0`, raise `ValueError`. If any assembled message exceeds the character limit, raise `ValueError` before returning any messages. The caller can regenerate a shorter reading before sending; do not truncate, silently omit sections, or send a partial result. A message exactly at the limit is allowed.

This task uses Python string length as its explicit budget. It does not model every Discord payload/Unicode edge case, generate a reading, or perform network sends.

Run `python -m unittest -v test_smoke.py`. Four groups worth 25 points each: grouping/order; preservation/boundary; overflow; schema validation.
