/* UNEXECUTED pure-JS proposal. No Node imports, atob, TextDecoder, streams or API calls. */
function decodeBase64Exact(input) {
  if (typeof input !== "string") throw new Error("base64 must be text");
  const s = input.replace(/[\t\r\n ]/g, ""), alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  if (s.length % 4) throw new Error("base64 length");
  const padding = s.endsWith("==") ? 2 : s.endsWith("=") ? 1 : 0;
  const size = s.length / 4 * 3 - padding;
  if (!Number.isSafeInteger(size) || size < 0) throw new Error("base64 size");
  const out = new Uint8Array(size); let op = 0;
  for (let ip = 0; ip < s.length; ip += 4) {
    const a = alphabet.indexOf(s[ip]), b = alphabet.indexOf(s[ip + 1]);
    const c = s[ip + 2] === "=" ? -2 : alphabet.indexOf(s[ip + 2]);
    const d = s[ip + 3] === "=" ? -2 : alphabet.indexOf(s[ip + 3]);
    const last = ip + 4 === s.length;
    if (a < 0 || b < 0 || c === -1 || d === -1) throw new Error("base64 alphabet");
    if (c === -2 && (!last || d !== -2 || (b & 15))) throw new Error("base64 double padding");
    if (c >= 0 && d === -2 && (!last || (c & 3))) throw new Error("base64 single padding");
    if (op >= out.length) throw new Error("base64 output overflow");
    out[op++] = (a << 2) | (b >>> 4);
    if (c >= 0) {
      if (op >= out.length) throw new Error("base64 output overflow");
      out[op++] = ((b & 15) << 4) | (c >>> 2);
      if (d >= 0) {
        if (op >= out.length) throw new Error("base64 output overflow");
        out[op++] = ((c & 3) << 6) | d;
      }
    }
  }
  if (op !== out.length) throw new Error("base64 exact length mismatch");
  return out;
}

function encodeBase64Exact(bytes) {
  if (!(bytes instanceof Uint8Array)) throw new Error("bytes must be Uint8Array");
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  const chunks = []; let part = "";
  for (let i = 0; i < bytes.length; i += 3) {
    const a = bytes[i], b = i + 1 < bytes.length ? bytes[i + 1] : 0, c = i + 2 < bytes.length ? bytes[i + 2] : 0;
    part += alphabet[a >>> 2] + alphabet[((a & 3) << 4) | (b >>> 4)] +
      (i + 1 < bytes.length ? alphabet[((b & 15) << 2) | (c >>> 6)] : "=") +
      (i + 2 < bytes.length ? alphabet[c & 63] : "=");
    if (part.length >= 16384) { chunks.push(part); part = ""; }
  }
  if (part) chunks.push(part);
  return chunks.join("");
}

function decompressRawLZ4Exact(src, expectedSize) {
  if (!(src instanceof Uint8Array)) throw new Error("LZ4 input must be Uint8Array");
  if (!Number.isSafeInteger(expectedSize) || expectedSize < 0 || expectedSize > 0x7fffffff) throw new Error("LZ4 expected size");
  if (!src.length) throw new Error("LZ4 empty block encoding");
  const out = new Uint8Array(expectedSize); let ip = 0, op = 0;
  function extendedLength(initial) {
    let length = initial;
    if (initial === 15) {
      let byte;
      do {
        if (ip >= src.length) throw new Error("LZ4 truncated length extension");
        byte = src[ip++]; length += byte;
        if (length > expectedSize) throw new Error("LZ4 extended length exceeds output size");
      } while (byte === 255);
    }
    return length;
  }
  while (ip < src.length) {
    const token = src[ip++];
    const literals = extendedLength(token >>> 4);
    if (literals > src.length - ip || literals > expectedSize - op) throw new Error("LZ4 literal bounds");
    out.set(src.subarray(ip, ip + literals), op); ip += literals; op += literals;
    if (ip === src.length) {
      if (op !== expectedSize) throw new Error("LZ4 final exact-size mismatch");
      return out;
    }
    if (src.length - ip < 2) throw new Error("LZ4 truncated offset");
    const offset = src[ip] | (src[ip + 1] << 8); ip += 2;
    if (offset === 0 || offset > op) throw new Error("LZ4 invalid backreference");
    const match = extendedLength(token & 15) + 4;
    if (match > expectedSize - op) throw new Error("LZ4 match output bounds");
    for (let n = 0; n < match; n++) { out[op] = out[op - offset]; op++; }
    if (ip === src.length) throw new Error("LZ4 missing final literal sequence");
  }
  throw new Error("LZ4 missing final sequence");
}

function exactGitBlobBase64FromLZ4(base64Chunks, expectedRawBytes, expectedCompressedBytes) {
  if (!Array.isArray(base64Chunks) || base64Chunks.some(x => typeof x !== "string")) throw new Error("ordered base64 chunks required");
  const compressed = decodeBase64Exact(base64Chunks.join(""));
  if (!Number.isSafeInteger(expectedCompressedBytes) || compressed.length !== expectedCompressedBytes) throw new Error("compressed exact-size mismatch");
  return encodeBase64Exact(decompressRawLZ4Exact(compressed, expectedRawBytes));
}
