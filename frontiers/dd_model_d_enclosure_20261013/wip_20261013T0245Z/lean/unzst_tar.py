import sys, tarfile, zstandard
src, dst = sys.argv[1], sys.argv[2]
with open(src, 'rb') as fh:
    dctx = zstandard.ZstdDecompressor()
    with dctx.stream_reader(fh) as reader:
        with tarfile.open(fileobj=reader, mode='r|') as tf:
            n = 0
            for m in tf:
                tf.extract(m, dst, filter='tar')
                n += 1
print('members', n)
