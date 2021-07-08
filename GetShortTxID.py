#!/usr/bin/env python3

def GetShortTxID(shorttxidk0, shorttxidk1, txhash):

    def uint64(x):
        return x % 2 ** 64

    def SIPROUND(v0, v1, v2, v3):

        def ROTL(x, b):
            return uint64((x << b) | (x >> (64 - b)))

        v0 = uint64(v0 + v1)
        v1 = ROTL(v1, 13)
        v1 = uint64(v1 ^ v0)
        v0 = ROTL(v0, 32)
        v2 = uint64(v2 + v3)
        v3 = ROTL(v3, 16)
        v3 = uint64(v3 ^ v2)
        v0 = uint64(v0 + v3)
        v3 = ROTL(v3, 21)
        v3 = uint64(v3 ^ v0)
        v2 = uint64(v2 + v1)
        v1 = ROTL(v1, 17)
        v1 = uint64(v1 ^ v2)
        v2 = ROTL(v2, 32)
        return v0, v1, v2, v3

    def SipHashUint256(k0, k1, val):

        assert(len(val) == 64)
        d = uint64(int(val[48:64], 16))
        v0 = uint64(0x736f6d6570736575 ^ k0)
        v1 = uint64(0x646f72616e646f6d ^ k1)
        v2 = uint64(0x6c7967656e657261 ^ k0)
        v3 = uint64(0x7465646279746573 ^ k1 ^ d)

        v0, v1, v2, v3 = SIPROUND(v0, v1, v2, v3)
        v0, v1, v2, v3 = SIPROUND(v0, v1, v2, v3)
        v0 = uint64(v0 ^ d)
        d = uint64(int(val[32:48], 16))
        v3 = uint64(v3 ^ d)
        v0, v1, v2, v3 = SIPROUND(v0, v1, v2, v3)
        v0, v1, v2, v3 = SIPROUND(v0, v1, v2, v3)
        v0 = uint64(v0 ^ d)
        d = uint64(int(val[16:32], 16))
        v3 = uint64(v3 ^ d)
        v0, v1, v2, v3 = SIPROUND(v0, v1, v2, v3)
        v0, v1, v2, v3 = SIPROUND(v0, v1, v2, v3)
        v0 = uint64(v0 ^ d)
        d = uint64(int(val[0:16], 16))
        v3 = uint64(v3 ^ d)
        v0, v1, v2, v3 = SIPROUND(v0, v1, v2, v3)
        v0, v1, v2, v3 = SIPROUND(v0, v1, v2, v3)
        v0 = uint64(v0 ^ d)
        v3 = uint64(v3 ^ uint64(uint64(4) << 59))
        v0, v1, v2, v3 = SIPROUND(v0, v1, v2, v3)
        v0, v1, v2, v3 = SIPROUND(v0, v1, v2, v3)
        v0 = uint64(v0 ^ uint64(uint64(4) << 59))
        v2 = uint64(v2 ^ 0xFF)
        v0, v1, v2, v3 = SIPROUND(v0, v1, v2, v3)
        v0, v1, v2, v3 = SIPROUND(v0, v1, v2, v3)
        v0, v1, v2, v3 = SIPROUND(v0, v1, v2, v3)
        v0, v1, v2, v3 = SIPROUND(v0, v1, v2, v3)
        return uint64(v0 ^ v1 ^ v2 ^ v3)

    assert not (shorttxidk0 == 0 and shorttxidk1 == 0)
    return SipHashUint256(shorttxidk0, shorttxidk1, txhash) & 0xffffffffffffff
