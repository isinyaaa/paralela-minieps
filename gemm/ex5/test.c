/* Aqui é onde os testes são implementados */

#include "matrix.h"
#include "time_extra.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Se o seu processador tiver pouco cache (muito lento), talvez seja prático
 * diminuir esse número. Use uma pot. de 2
 */
#define N 512

int main()
{
    double *restrict A = aligned_alloc(8, N*N*sizeof(*A));
    double *restrict B = aligned_alloc(8, N*N*sizeof(*B));
    double *restrict C = aligned_alloc(8, N*N*sizeof(*C));

    srand(1337);
    matrix_fill_rand(N, A);
    matrix_fill_rand(N, B);

    memset(C, 0, N*N*sizeof(*C));
    matrix_which_dgemm(0, N, C, A, B);

    free(A);
    free(B);
    free(C);
}
