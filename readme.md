# myjson - a minimalist json parser and dumper

## How to use

```python
import myjson

assert myjson.load('{"key": "value"}') == {"key": "value"}

assert myjson.load('["value", "value2"]') == ["value", "value2"]

assert myjson.load("value") == "value"
```
