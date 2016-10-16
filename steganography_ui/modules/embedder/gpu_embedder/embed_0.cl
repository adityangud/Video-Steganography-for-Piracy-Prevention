int get_luma_index(int imgid, int nrows, int ncols, int npix, int x, int y)
{
    return ((imgid * nrows * ncols * npix) + (x * ncols * npix) + (y * npix));
}

int get_luma(int r, int g, int b){
    int luma = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    return luma;
}

__kernel void embed_zero(__global const uchar *a, __global uchar *c)
{
    // embedding one bit into the image
    int imgid = get_global_id(0);
    int rowid = get_global_id(1);
    int colid = get_global_id(2);

    int nrows = %d;
    int ncols = %d;
    int npix = %d;

    int current_index = get_luma_index(imgid, nrows, ncols, npix, rowid, colid);

    float r, g, b;
    int _r, _g, _b;
    float y, cb, cr;
    r = a[current_index];
    g = a[current_index + 1];
    b = a[current_index + 2];
    y = get_luma(r,g,b);
    cb = -0.09991 * r - 0.33609 * g + 0.436 * b;
    cr = 0.615 * r - 0.55861 * g -0.05639 * b;

    /* finding that value v */
    int laplacian_sum = 0;

    int xm1_ym1 = get_luma_index(imgid, nrows, ncols, npix, rowid-1, colid-1);
    int x_ym1 = get_luma_index(imgid, nrows, ncols, npix, rowid, colid-1);
    int xp1_ym1 = get_luma_index(imgid, nrows, ncols, npix, rowid+1, colid-1);

    int xm1_y = get_luma_index(imgid, nrows, ncols, npix, rowid-1, colid);
    int x_y = get_luma_index(imgid, nrows, ncols, npix, rowid, colid);
    int xp1_y = get_luma_index(imgid, nrows, ncols, npix, rowid+1, colid);

    int xm1_yp1 = get_luma_index(imgid, nrows, ncols, npix, rowid-1, colid+1);
    int x_yp1 = get_luma_index(imgid, nrows, ncols, npix, rowid, colid+1);
    int xp1_yp1 = get_luma_index(imgid, nrows, ncols, npix, rowid+1, colid+1);

    laplacian_sum += 8 * a[x_y];
    if( colid != 0 ) laplacian_sum -= a[xm1_y];
    if( colid != (ncols - 1)) laplacian_sum -= a[xp1_y];

    if( rowid != 0){
        laplacian_sum -= a[x_ym1];
        if( colid != 0 ) laplacian_sum -= a[xm1_ym1];
        if( colid != (ncols - 1)) laplacian_sum -= a[xp1_ym1];
    }

    if( rowid != (nrows - 1)){
        laplacian_sum -= a[x_yp1];
        if( colid != 0 ) laplacian_sum -= a[xm1_yp1];
        if( colid != (ncols - 1)) laplacian_sum -= a[xp1_yp1];
    }

    float laplacian_factor = 0.25f * (float)laplacian_sum;
    int l_value = (int)(laplacian_factor + 0.5);
    if(l_value < 0) l_value = -1 * l_value;

    int u_min = 3;
    int prev_img_luma_index = current_index;
    if(imgid != 0) prev_img_luma_index = get_luma_index(imgid-1, nrows, ncols, npix, rowid, colid);

    int prev_img_luma = get_luma(a[prev_img_luma_index], a[prev_img_luma_index + 1], a[prev_img_luma_index + 2]);
    int luma_diff = y - prev_img_luma;
    if( luma_diff < 0) luma_diff = -1 * luma_diff;

    int u = u_min + luma_diff;

    int v = (u < l_value)? u : l_value;

    /* found that value v */
    if(v < 0) v  = -1 * v;

    y = y - 8;
    if ( y < 0 ) y = 0;

    r = y + 1.28033 * cr;
    g = y - 0.21482 * cb - 0.38059 * cr;
    b = y + 2.12798 * cb;


    _r = (int) r;
    _g = (int) g;
    _b = (int) b;

    if(_r > 255) _r = 255;
    if(_r < 0 ) _r = 0;

    if(_g > 255) _g = 255;
    if(_g < 0 ) _g = 0;

    if(_b > 255) _b = 255;
    if(_b < 0 ) _b = 0;

    c[current_index] = _r;
    c[current_index + 1] = _g;
    c[current_index + 2] = _b;
}
