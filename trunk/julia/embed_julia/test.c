#include <julia.h>
JULIA_DEFINE_FAST_TLS // only define this once, in an executable (not in a shared library) if you want fast code.

int main(int argc, char *argv[])
{
    /* required: setup the Julia context */
    jl_init();

    /* run Julia commands */
    jl_eval_string("println(sqrt(2.0))");
    jl_value_t *ret = jl_eval_string("sqrt(2.0)");
    if (jl_typeis(ret, jl_float64_type)) {
        double ret_unboxed = jl_unbox_float64(ret);
        printf("sqrt(2.0) from Julia: %e \n", ret_unboxed);
    }
    else {
        printf("ERROR: unexpected return type from sqrt(::Float64)\n");
    }
    
    // In the first step, a handle to the Julia function sqrt is retrieved by calling jl_get_function.
    // The first argument passed to jl_get_function is a pointer to the Base module in which sqrt is defined.
    // Then, the double value is boxed using jl_box_float64.
    // Finally, in the last step, the function is called using jl_call1. 
    // jl_call0, jl_call2, and jl_call3 functions also exist, to conveniently handle different numbers of arguments.
    // To pass more arguments, use jl_value_t *jl_call(jl_function_t *f, jl_value_t **args, int32_t nargs).
    jl_function_t *func = jl_get_function(jl_base_module, "sqrt");
    jl_value_t *argument = jl_box_float64(2.0);
    jl_value_t *ret_1 = jl_call1(func, argument);


    // Alternative and simpler way: first define a C callable function in Julia, extract the function pointer from it;
    // and finally call it.
    double (*sqrt_jl)(double) = jl_unbox_voidpointer(jl_eval_string("@cfunction(sqrt, Float64, (Float64,))"));
    double ret_2 = sqrt_jl(2.0);
    printf("sqrt(2.0) via Julia @cfunction: %e \n", ret_2);

    /* strongly recommended: notify Julia that the
         program is about to terminate. this allows
         Julia time to cleanup pending write requests
         and run all finalizers
    */
    jl_atexit_hook(0);
    return 0;
}
