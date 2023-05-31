## Isabella Basso - 11810773

# Mini EP 6

In this exercise we, again, take advantage of memory layout (cache locality) to
speed up matrix multiplication. This time we implement a very simple blocking
technique, which we lay out below:

0. We start from the previous exercise, where we had a simple matrix
   multiplication algorithm that didn't take advantage of cache size.

    ```c
    void matrix_dgemm_2(int n, double *restrict _C,
                        double *restrict _A, double *restrict _B)
    {
        #define A(i, j) _A[n*(i) + (j)]
        #define B(i, j) _B[n*(i) + (j)]
        #define C(i, j) _C[n*(i) + (j)]

        int i, j, k;

        // unchanged
        for (i = 0; i < n; i++)
            for (k = 0; k < n; k++)
                for (j = 0; j < n; j++)
                    C(i, j) += A(i, k) * B(k, j);

        #undef A
        #undef B
        #undef C
    }
    ```

1. We define a macro to hold our desired block size (`bs`). To accomplish
   blocking we change our initial loops to use the block size.

    ```c
    void matrix_dgemm_2(int n, double *restrict _C,
                        double *restrict _A, double *restrict _B)
    {
        #define A(i, j) _A[n*(i) + (j)]
        #define B(i, j) _B[n*(i) + (j)]
        #define C(i, j) _C[n*(i) + (j)]
        #define bs 4

        int i, j, k;

        /* we iterate in bs steps now, so we are skipping n - n/bs elements */
        for (i = 0; i < n; i += bs)
            for (k = 0; k < n; k += bs)
                for (j = 0; j < n; j += bs)
                    /* we need an inner routine to complete the computation */
                    // C(i, j) += A(i, k) * B(k, j);

        #undef A
        #undef B
        #undef C
    }
    ```

    > Notice that we're skipping lots of elements in this computation, so this
    > time we need to provide an inner routine to complete the computation.

2. This approach gives us lots of options to optimize memory handling, though,
   fortunately, a very simple one will work. We need simply to iterate over the
   elements in each block, performing our original computation as if we had a
   smaller (square) matrix of side length `bs`.

    ```c
    void matrix_dgemm_2(int n, double *restrict _C,
                        double *restrict _A, double *restrict _B)
    {
        #define A(i, j) _A[n*(i) + (j)]
        #define B(i, j) _B[n*(i) + (j)]
        #define C(i, j) _C[n*(i) + (j)]
        #define bs 4

        int i, j, k, i_block, j_block, k_block;

        for (i_block = 0; i_block < n; i_block += bs)
            for (k_block = 0; k_block < n; k_block += bs)
                for (j_block = 0; j_block < n; j_block += bs)
                    for (i = i_block; i < i_block + bs; i++)
                        for (k = k_block; k < k_block + bs; k++)
                            for (j = j_block; j < j_block + bs; j++)
                                C(i, j) += A(i, k) * B(k, j);

        #undef A
        #undef B
        #undef C
    }
    ```

    > Notice that the inner loop could be optimized to use a fixed block size
    > and load its data directly into registers, but that's out of the scope of
    > this exercise.

3. We can test this code now to see we indeed get about half the runtime when
   compared to the previous version.

Finally, we add `bs` as a parameter for the function, and also make
modifications to `matrix_which_dgemm` to be able to test various block sizes.

Plotting relative performance between the previous version and this one, we
obtain the following graphs:

![Relative performance on an `x86-64` machine](./plots/x86_64-gemm.png)
![Relative performance on an `aarch64` machine](./plots/aarch64-gemm.png)

The `x86-64` results refer to a Ryzen 7 5800X CPU, while the `aarch64` results
refer to a MacBook Pro M1. We can see that we get the expected results on
the `x86-64` machine, but the `aarch64` machine seems to be have better
optimizations for the previous version of the code. This is probably due to
architectural differences that the compiler handles better than we do.

The code used to generate the graphs is available at [`plot.py`](./plot.py).
