__kernel void calc_luma(__global const uchar *a, __global long *c)
{
    int imgid = get_global_id(0);

    int nrows = %d;
    int ncols = %d;
    int npix = %d;

    int i,j, luma_index, rowid;
    int img_index = imgid * nrows * ncols * npix;

    int r,g, b;

    long total_luma = 0;
    for(i=0; i < nrows; i++){
            rowid = i * ncols * npix;
            for(j=0; j < ncols; j++){
                luma_index = img_index + rowid  + j * npix;
                r = a[luma_index];
                g = a[luma_index + 1];
                b = a[luma_index + 2];
                total_luma += (long)(0.2126 * r + 0.7152 * g + 0.0722 * b);
            }
    }
    c[imgid] = (total_luma);
}
