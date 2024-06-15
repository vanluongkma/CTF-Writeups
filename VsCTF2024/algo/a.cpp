#include <iostream>
#include <vector>
using namespace std;

const int MOD = 1000000007;

int count_valid_permutations(int n) {
    if (n == 1) return 1;

    vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));

    // Base case: Any single element is a valid sequence
    for (int j = 1; j <= n; ++j) {
        dp[1][j] = 1;
    }

    for (int i = 2; i <= n; ++i) {
        if (i % 2 == 1) {
            // i is odd: We need a[i-1] < a[i]
            for (int j = 1; j <= n; ++j) {
                dp[i][j] = 0;
                for (int k = 1; k < j; ++k) {
                    dp[i][j] = (dp[i][j] + dp[i-1][k]) % MOD;
                }
            }
        } else {
            // i is even: We need a[i-1] > a[i]
            for (int j = 1; j <= n; ++j) {
                dp[i][j] = 0;
                for (int k = j + 1; k <= n; ++k) {
                    dp[i][j] = (dp[i][j] + dp[i-1][k]) % MOD;
                }
            }
        }
    }

    int result = 0;
    for (int j = 1; j <= n; ++j) {
        result = (result + dp[n][j]) % MOD;
    }

    return result;
}

int main() {
    int n;
    cin >> n;
    cout << count_valid_permutations(n) << endl;
    return 0;
}