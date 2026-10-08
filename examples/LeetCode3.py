class Solution:

    def lengthOfLongestSubstring(self, s: str) -> int:
        max_length = 0
        strt_idx = 0
        d = dict()

        for curr_idx, n in enumerate(s):

            if n in d:
                if d[n] >= strt_idx:
                    strt_idx = d[n] + 1
            d[n] = curr_idx

            max_length = max(curr_idx - strt_idx+1, max_length)


        return max_length


if __name__ == "__main__":
    s = "bbbbb"
    expcted = 1
    ans = Solution().lengthOfLongestSubstring(s)
    print(ans)
    assert ans == expcted


    s = "1R1T7"
    expcted = 4
    ans = Solution().lengthOfLongestSubstring(s)
    print(ans)
    assert ans == expcted

    s = "abcabcbb"
    expcted = 3
    ans = Solution().lengthOfLongestSubstring(s)
    print(ans)
    assert ans == expcted