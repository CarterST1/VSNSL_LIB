
from .VSNSL_LIB import VSNSL  # Use relative import if in the same package

vsnsl: VSNSL = VSNSL(1)

print(vsnsl.encodeData("abc"))
# Returns: "101102103"

print(vsnsl.decodeData("101102103"))
# Returns: "abc"

print(vsnsl.encodeBatch(["abc", "def", "ghi"]))
# Returns: ["101102103", "104105106", "107108109"]

print(vsnsl.decodeBatch(["101102103", "104105106", "107108109"]))
# Returns: ["abc", "def", "ghi"]

encryptedLocks = [1,2,3]
encrypted = vsnsl.mltEncode(encryptedLocks, "hi")
print(encrypted)
print(vsnsl.mltDecode(encryptedLocks, encrypted))