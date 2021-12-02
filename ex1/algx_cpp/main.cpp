#include <iostream>
#include <fstream>
#include <iomanip>
#include <bitset>
#include <vector>
#include <algorithm>
#include <sstream>

std::ostream &operator<<(std::ostream &os, std::vector<unsigned> &vec)
{
    for (unsigned e : vec)
        os << e << ", ";
    return os;
}

/// Circular shuffle
/// First, a copy of u shifted by one to the left is created,
/// then the LSB (position = 0) of the copy is set to
/// the value of the MSB (position = size(u) - 1)
///
/// In case you are unfamiliar with std::bitset:
/// std::bitset<L> creates a bit sequence of length L.
/// E.g.:
///     std::bitset<3> u(3); // u = 011
///     u[0]; // <==> LSB(u) = 1
///     u[3-1]; // <==> MSB(u) = 0
/// Ref: https://en.cppreference.com/w/cpp/utility/bitset
template <unsigned L>
std::bitset<L> shuffle(std::bitset<L> u)
{
    return (u << 1).set(/* position = */ 0, /* value_to_set = */ u[L - 1]);
}

template <unsigned L>
std::vector<unsigned> algorithm_x(unsigned i, unsigned j, unsigned num_nodes)
{
    // Arguably these checks should be done here.
    // For efficiency reasons to generate the data, these checks are ommitted or done externally (i.e. i and j are selected such that these cases do not appear)!
    // if (i >= num_nodes or j >= num_nodes)
    // {
    //     std::cout << "i or j too large!\n";
    //     return std::move(std::vector<unsigned>{i});
    // }
    // if (i == j)
    //     return std::move(std::vector<unsigned>{i});

    // X1
    std::bitset<L> u(i);
    unsigned e = L - 1;

    std::bitset<L> v(i);
    const std::bitset<L> j_bits(j); // order: bd-1 ... b1 b0
    constexpr std::bitset<L> bits_one(1);

    std::vector<unsigned> path{i};

    // for (unsigned e = L - 1; e >= 0; --e)
    while (e >= 0)
    {
        // # X2: b
        bool b = u[0]; // u[0] is the LSB(u)

        // # X3: Exchange
        // bool b_prime_e = j_bits[e];

        if (b != j_bits[e])
        {
            // Cause of 'u <- v' at the end we can change this:
            // v = u ^ bits_one;
            // path.push_back(v.to_ulong());
            // if (v == j_bits)
            //     return path;
            // u = v;
            // To this for minor efficiency reasons
            u ^= bits_one; // in place bxor to omit 1 copy
            path.push_back(u.to_ulong());
            if (u == j_bits)
                return path;
        }
        else
        {
            v = u;
        }

        // X4: Shuffle
        v = shuffle<L>(u); // circular shift
        if (v != u)
        {
            path.push_back(v.to_ulong());
            u = v;
            // # X5:
            if (u == j_bits)
                return path;
        }
        --e;
    }
    return path;
}

// #define UNIQUE_CHECK
// #define D 3
// #if D > 3
// #undef UNIQUE_CHECK
// #endif

template <unsigned D>
bool test_algx()
{
    const unsigned num_nodes = 1 << D;

    std::vector<unsigned> report(num_nodes, 0);
    unsigned errors = 0;
    unsigned num_tests = 0;
#ifdef UNIQUE_CHECK
    unsigned removed = 0;
#endif

    std::cout << "d: " << D << "\n";
    std::cout << "num_nodes: " << num_nodes << "\n";
    for (unsigned i = 0; i < num_nodes; ++i)
    {
        for (unsigned j = 0; j < num_nodes; ++j)
        {
            if (i != j)
            {
                std::vector<unsigned> path = algorithm_x<D>(i, j, num_nodes);
                // std::cout << i << " -> " << j << ": " << path << std::endl;
                if (path.back() != j)
                    ++errors;
                unsigned path_length = path.size();
                // path_length = (path_length > num_nodes - 1) ? path_length : num_nodes - 1;
                report[path_length] += 1;
                ++num_tests;
#ifdef UNIQUE_CHECK
                // sort followed by unique, to remove all duplicates
                std::sort(path.begin(), path.end());
                auto last = std::unique(path.begin(), path.end());
                if (path.end() - last != 0)
                {
                    ++removed;
                    //// Paths with duplicate entries, i.e. loops, can be shown this way...
                    //// BUT, everything past 'last' is indeterminate!
                    // std::cout << i << " -> " << j << ": " << path << std::endl;
                }
#endif
            }
        }
    }
    // unsigned i = 1, j = 4;
    // std::vector<unsigned> path = algorithm_x<D>(i, j, num_nodes);
    // std::cout << i << " -> " << j << ": " << path << std::endl;

    unsigned check_tests = 0;
    for (auto &counted : report)
        check_tests += counted;
    if (num_tests != check_tests)
        std::cout << "ERROR\n";
    const unsigned passed = num_tests - errors;
    unsigned coverage = (passed / num_tests) * 100;

    std::cout << "PASSED: " << passed << "/" << num_tests << " [coverage: " << coverage << "%]\n";
#ifdef UNIQUE_CHECK
    std::cout << "LOOPLESS PATHS: " << num_tests - removed << "/" << num_tests << "\n";
#endif

    std::stringstream fname;
    fname << "binned_path_lengths_" << D << ".csv";

    std::ofstream file(fname.str(), std::ios::out | std::ios::trunc);
    file << report << "\n";

    std::cout << "------------------\n";

    return passed == num_tests;
}

template <typename... Args>
bool all(Args... args)
{
    return (... && args);
}

int main(int argc, char **argv)
{

    bool test5 = test_algx<5>();
    bool test10 = test_algx<10>();
    bool test12 = test_algx<12>();
    bool test15 = test_algx<15>();

    // return (test5 && test10 && test12) ? EXIT_SUCCESS : EXIT_FAILURE;
    return all(test5, test10, test12, test15) ? EXIT_SUCCESS : EXIT_FAILURE;
}