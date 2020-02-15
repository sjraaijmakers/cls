import numpy as np
import pyopencl as cl
import pyopencl.cltypes
from numba import njit, prange
import time
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


#############################
# Setup context, queue and memflags on gpu
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
mf = cl.mem_flags
##############################

@njit
def gen_complex_vals(NUM_POINTS):
    complex_vals = []
    for _ in range(NUM_POINTS):
        complex_vals.append((np.random.uniform(-2, 2), np.random.uniform(-2, 2), 0, 0))
    return complex_vals

def mandelbrot_on_gpu(NUM_POINTS=100000, max_iter=1000):
    # mandelbrot kernel
    global ctx
    global queue
    global mf

    prg = cl.Program(ctx, """
    __kernel void mandelbrot(__global float4 *c, __global float4 *output, ushort const max_iter){
        int gid = get_global_id(0);

        // set the datapoints back into the vector. By default all points are mandel until they are not.
        output[gid].x = c[gid].x;
        output[gid].y = c[gid].y;
        output[gid].z = 1;
        output[gid].w = max_iter;

        float real = c[gid].x;
        float imag = c[gid].y;
        for(int i = 0; i < max_iter; i++) {
            float real2 = real*real, imag2 = imag*imag;
            if (real*real + imag*imag > 4.0f){
                    output[gid].z = 0; // point is not mandel
                    output[gid].w = i; // return its itter point found in the vector
                    return;
            }
            imag = 2* real*imag + c[gid].y;
            real = real2 - imag2 + c[gid].x;
        }
    }
    """).build()

    # Data and buffer (given complex vals)
    c_np = np.asarray(gen_complex_vals(NUM_POINTS), dtype=cl.cltypes.float4)
    c_opencl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=c_np)

    # Data and buffer (for output)
    output_np = np.zeros(c_np.shape, dtype=cl.cltypes.float4)
    output_opencl = cl.Buffer(ctx, mf.WRITE_ONLY, output_np.nbytes)

    # run mandelbrot and copy gpu output into output_np array
    prg.mandelbrot(queue, output_np.shape, None, c_opencl, output_opencl, np.uint16(max_iter))
    cl.enqueue_copy(queue, output_np, output_opencl).wait()

    return output_np

def filter_points(output_np, max_iter):
    points = []
    colors = []

    for vals in output_np:
        points.append(complex(vals[0], vals[1]))
        colors.append(np.log10(vals[3] + 1)) # used for the cmap

    return np.asarray(points), np.asarray(colors)


def run(plot=False):
    start_time = time.time()

    N = 10000000
    max_iter = 10000

    # filter points which aren't mandelbrot
    points = mandelbrot_on_gpu(N, max_iter)

    print("Finished running sim...")
    print("Ordering data...")
    points, colors = filter_points(points, max_iter)
    print("Finished, calling plotter...")

    if plot:
        plt.scatter(points.real, points.imag, s=1, c=colors, cmap="inferno")
        plt.show()
        # plt.savefig("colorized.pdf")


if __name__ == "__main__":
    run(True)
