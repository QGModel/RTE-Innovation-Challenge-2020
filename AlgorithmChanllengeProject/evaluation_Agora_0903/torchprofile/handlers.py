from .utils import math

__all__ = ['handlers']


def addmm(node):
    # [n, p] = aten::addmm([n, p], [n, m], [m, p], *, *)
    n, m = node.inputs[1].shape
    m, p = node.inputs[2].shape
    return n * m * p


def addmv(node):
    # [n] = aten::addmv([n], [n, m], [m], *, *)
    n, m = node.inputs[1].shape
    return n * m


def bmm(node):
    # [b, n, p] = aten::bmm([b, n, m], [b, m, p])
    b, n, m = node.inputs[0].shape
    b, m, p = node.inputs[1].shape
    return b * n * m * p


def matmul(node):
    if node.inputs[0].ndim == 1 and node.inputs[1].ndim == 1:
        # [] = aten::matmul([n], [n])
        n = node.inputs[0].shape[0]
        return n
    elif node.inputs[0].ndim == 1 and node.inputs[1].ndim == 2:
        # [m] = aten::matmul([n], [n, m])
        n, m = node.inputs[1].shape
        return n * m
    elif node.inputs[0].ndim == 2 and node.inputs[1].ndim == 1:
        # [n] = aten::matmul([n, m], [m])
        n, m = node.inputs[0].shape
        return n * m
    elif node.inputs[0].ndim == 2 and node.inputs[1].ndim == 2:
        # [n, p] = aten::matmul([n, m], [m, p])
        n, m = node.inputs[0].shape
        m, p = node.inputs[1].shape
        return n * m * p
    elif node.inputs[0].ndim == 1:
        # [..., m] = aten::matmul([n], [..., n, m])
        *b, n, m = node.inputs[1].shape
        return math.prod(b) * n * m
    elif node.inputs[1].ndim == 1:
        # [..., n] = aten::matmul([..., n, m], [m])
        *b, n, m = node.inputs[0].shape
        return math.prod(b) * n * m
    else:
        # [..., n, p] = aten::matmul([..., n, m], [..., m, p])
        *b, n, p = node.outputs[0].shape
        *_, n, m = node.inputs[0].shape
        *_, m, p = node.inputs[1].shape
        return math.prod(b) * n * m * p


def mul(node):
    os = node.outputs[0].shape
    return math.prod(os)


def convolution(node):
    if node.outputs[0].shape[1] == node.inputs[1].shape[0]:
        oc, ic, *ks = node.inputs[1].shape
    else:
        ic, oc, *ks = node.inputs[1].shape
    os = node.outputs[0].shape
    return math.prod(os) * ic * math.prod(ks)

def transpose(node):
    os = node.outputs[0].shape
    return math.prod(os)

def prelu(node):
    os = node.outputs[0].shape

    return math.prod(os)
def pixel_shuffle(node):
    os = node.outputs[0].shape

    return math.prod(os)
def batch_norm(node):
    os = node.outputs[0].shape

    return 2*math.prod(os)

def ada_pool(node):
    #oc, ic, *ks = node.inputs[0].shape
    os = node.outputs[0].shape
    return math.prod(os)
def cat(node):
    os = node.outputs[0].shape
    return math.prod(os)

def instance_norm_or_layer_norm(node):
    os = node.outputs[0].shape
    return math.prod(os)


def avg_pool_or_mean(node):
    os = node.outputs[0].shape
    return math.prod(os)


handlers = (
    ('aten::addmm', addmm), ('aten::addmv', addmv), ('aten::bmm', bmm),
    ('aten::matmul', matmul), (('aten::mul', 'aten::mul_'), mul),
    ('aten::_convolution', convolution),
    ('aten::transpose', transpose),
    ('aten::batch_norm', batch_norm),
    (('aten::instance_norm', 'aten::layer_norm'),
     instance_norm_or_layer_norm),
    (('aten::prelu','aten::relu', 'aten::leaky_relu_', 'aten::relu_','aten::clamp_',
       'aten::round','aten::threshold','aten::view' ), prelu),
    ('aten::pixel_shuffle', pixel_shuffle),
    (('aten::adaptive_avg_pool1d', 'aten::adaptive_avg_pool2d',
      'aten::adaptive_avg_pool3d', 'aten::avg_pool1d', 'aten::avg_pool2d',
      'aten::avg_pool3d', 'aten::mean'), avg_pool_or_mean),
    (('aten::adaptive_max_pool1d', 'aten::adaptive_max_pool2d',
      'aten::adaptive_max_pool3d'), ada_pool),
    ('aten::cat', cat),
    (( 'aten::add', 'aten::add_',
      'aten::alpha_dropout', 'aten::chunk', 'aten::clamp',
      'aten::clone', 'aten::constant_pad_nd', 'aten::contiguous', 'aten::div',
      'aten::div_', 'aten::dropout', 'aten::dropout_', 'aten::embedding',
      'aten::eq', 'aten::feature_dropout', 'aten::flatten', 'aten::gt',
      'aten::hardtanh_', 'aten::int', 'aten::lt', 'aten::log_softmax',
      'aten::max_pool1d', 'aten::max_pool1d_with_indices', 'aten::max_pool2d',
      'aten::max_pool2d_with_indices', 'aten::max_pool3d',
      'aten::max_pool3d_with_indices', 'aten::max_unpool1d',
      'aten::max_unpool2d', 'aten::max_unpool3d', 'aten::ne',
      'aten::reflection_pad1d', 'aten::reflection_pad2d',
      'aten::reflection_pad3d',
      'aten::replication_pad1d', 'aten::replication_pad2d',
      'aten::replication_pad3d', 'aten::rsub', 'aten::select', 'aten::sigmoid',
      'aten::size', 'aten::slice', 'aten::softmax', 'aten::softshrink',
      'aten::squeeze', 'aten::sub', 'aten::sum', 'aten::t', 'aten::tanh',
      'aten::view', 'aten::zeros',
      'prim::constant', 'prim::listconstruct', 'prim::listunpack',
      'prim::numtotensor', 'prim::tupleconstruct','aten::split_with_sizes',
       ), None))
