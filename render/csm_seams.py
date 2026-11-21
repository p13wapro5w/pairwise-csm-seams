def cascade_index(distance, splits):
    """级联选择：按屏幕误差划分后的 split 距离选择级联。

    距离落在第一个不小于它的 split 边界所属级联内；超出远平面时钳制到
    最后一级，不再按相机距离做无保护的硬切（实际切换需配合 hysteresis）。
    """
    for i, boundary in enumerate(splits):
        if distance <= boundary:
            return i
    return len(splits) - 1


def split_ranges(splits):
    """级联区间：把按屏幕误差算出的 split 距离展开成 (near, far) 区间序列。"""
    ranges = []
    prev = 0
    for boundary in splits:
        ranges.append((prev, boundary))
        prev = boundary
    return ranges


def hysteresis(prev, candidate, threshold):
    """级联滞回：候选级联与当前级联差距达到阈值才切换，避免交界处来回跳层。"""
    if abs(candidate - prev) >= threshold:
        return candidate
    return prev


def texel_world_size(extent, resolution):
    """texel 世界尺寸：正交光相机覆盖 [-extent, +extent]，世界跨度为 2*extent。

    每一级联用自己的 extent 计算，远级联 texel 更粗，偏移量必须基于该值
    而不是全局固定尺寸。
    """
    return (2.0 * extent) / resolution


def filter_kernel(level, base):
    """统一滤波核：所有级联使用同一族 PCF 核，核半径按 2^level 缩放。

    禁止级联间 PCF/ESM 混用，消除半影像素化方块。
    """
    return base * (2 ** level)


def layer_index(level):
    """阴影数组层：层索引即级联编号，层内 texel 偏移由分辨率换算而非写死。"""
    return level


def update_levels(max_level):
    """动态物体逐级更新：从第 0 级到 max_level 全部刷新，远处角色不再丢影子。"""
    return list(range(max_level + 1))


def penumbra_scale(radius, level):
    """半影按级联缩放：世界空间滤波半径除以 2^level，交界处两边软硬一致。"""
    return radius / (2 ** level)


def inside_bounds(bounds, point):
    """包围盒包含：级联包围球/盒按相机朝向收紧后，判定边缘物体是否仍在图内。"""
    x0, y0, x1, y1 = bounds
    x, y = point
    return bool(x0 <= x <= x1 and y0 <= y <= y1)


def depth_bias(texel, slope):
    """阴影偏移：按当前级联 texel 世界尺寸做斜率缩放，远级联不再大面积 acne。"""
    return texel * slope


def cascade_count(splits):
    """级联数量：split 边界数即级联数。"""
    return len(splits)


def jitter_offset(frame, levels):
    """远级联时间抖动：在 levels 个子 texel 位置间周期轮换，摊薄低频更新闪烁。"""
    return (frame % levels) / levels


def shadow_key(camera, level):
    """阴影键：按相机与级联编号唯一标识一份阴影贴图缓存。"""
    return "{}:{}".format(camera, level)


def clamp_cascade(index, count):
    """级联钳制：索引约束在 [0, count-1]，防止采样越界到不存在的数组层。"""
    return max(0, min(index, count - 1))


def cascade_extent(near, far):
    """级联范围：视锥片段的深度跨度，供按屏幕误差划分与 pancaking 压扁使用。"""
    return far - near
