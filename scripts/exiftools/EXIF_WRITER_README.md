# ExifWriter 工具类使用说明

`exif_writer.py` 是一个 Python 工具类，用于批量修改视频和图片文件的 EXIF 元数据。

## 功能特性

- ✅ 支持视频文件（MP4, MOV, M4V, AVI, MKV 等）
- ✅ 支持图片文件（JPG, PNG, HEIC, TIFF 等）
- ✅ 设置 GPS 坐标（经纬度、海拔）
- ✅ 设置设备信息（制造商、型号、软件版本）
- ✅ 设置创建日期/时间
- ✅ 自动处理时区转换（视频文件 UTC 时间）
- ✅ 批量处理多个文件
- ✅ 支持方法链式调用
- ✅ 支持命令行接口

## 安装要求

1. Python 3.6+
2. exiftool（需要安装并添加到 PATH，或指定路径）

### 安装 exiftool

- Windows: 下载 [exiftool](https://exiftool.org/) 并解压，将 `exiftool.exe` 添加到 PATH
- macOS: `brew install exiftool`
- Linux: `sudo apt-get install libimage-exiftool-perl` 或 `sudo yum install perl-Image-ExifTool`

## 基本使用

### 作为 Python 模块使用

```python
from exif_writer import ExifWriter

# 创建写入器实例
writer = ExifWriter()

# 设置 GPS 坐标
writer.set_gps(lat=34.673500, lon=112.492300, alt=138.848)

# 设置设备信息
writer.set_device(make="Apple", model="iPhone 14 Plus", software="18.6")

# 设置创建日期（本地时间，视频会自动转换为 UTC）
writer.set_creation_date("2024:01:15 14:30:00", timezone_offset_hours=8)

# 写入到文件
success, stdout, stderr = writer.write("video.mp4")

if success:
    print("成功！")
else:
    print(f"失败: {stderr}")
```

### 方法链式调用

```python
writer = (ExifWriter()
          .set_gps(lat=34.673500, lon=112.492300, alt=138.848)
          .set_device(make="Apple", model="iPhone 14 Plus")
          .set_accuracy(5.0)
          .set_creation_date("2024:01:15 14:30:00"))

success, stdout, stderr = writer.write("video.mp4")
```

### 批量处理

```python
writer = ExifWriter()
writer.set_gps(lat=34.673500, lon=112.492300)
writer.set_device(make="Apple", model="iPhone 14 Plus")
writer.set_creation_date("2024:01:15 14:30:00")

files = ["video1.mp4", "video2.mp4", "image1.jpg"][de.vbs](..%2F..%2F..%2F..%2F%CF%EE%C4%BF%CE%C4%B5%B5%2F%B3%E4%B5%E7%B9%F11.8.2%BE%D6%D3%F2%CD%F8%2Fde.vbs)
results = writer.write_batch(files)

for filepath, success, stdout, stderr in results:
    if success:
        print(f"✓ {filepath}")
    else:
        print(f"✗ {filepath}: {stderr}")
```

### 重置和重用

```python
writer = ExifWriter()

# 处理第一个文件
writer.set_gps(lat=34.673500, lon=112.492300)
writer.write("file1.mp4")

# 重置并处理第二个文件
writer.reset()
writer.set_gps(lat=40.7128, lon=-74.0060)  # 纽约
writer.write("file2.mp4")
```

## 命令行使用

```bash
# 基本用法
python exif_writer.py video.mp4 --lat 34.673500 --lon 112.492300 --alt 138.848

# 完整参数
python exif_writer.py video.mp4 \
    --lat 34.673500 \
    --lon 112.492300 \
    --alt 138.848 \
    --make "Apple" \
    --model "iPhone 14 Plus" \
    --software "18.6" \
    --accuracy 5.0 \
    --date "2024:01:15 14:30:00" \
    --timezone-offset 8

# 预览命令（不实际执行）
python exif_writer.py video.mp4 --lat 34.673500 --lon 112.492300 --dry-run

# 指定 exiftool 路径
python exif_writer.py video.mp4 --lat 34.673500 --lon 112.492300 --exiftool "C:\Tools\exiftool.exe"
```

## API 参考

### ExifWriter 类

#### 构造函数

```python
ExifWriter(exiftool_path: Optional[str] = None)
```

- `exiftool_path`: 可选的 exiftool 可执行文件路径。如果不提供，会在 PATH 中查找。

#### 方法

##### `set_gps(lat: float, lon: float, alt: float = 0.0) -> ExifWriter`

设置 GPS 坐标。

- `lat`: 纬度（-90 到 90）
- `lon`: 经度（-180 到 180）
- `alt`: 海拔高度（米），默认 0.0

##### `set_device(make: Optional[str] = None, model: Optional[str] = None, software: Optional[str] = None) -> ExifWriter`

设置设备信息。

- `make`: 制造商（如 "Apple"）
- `model`: 型号（如 "iPhone 14 Plus"）
- `software`: 软件版本（如 "18.6"）

##### `set_accuracy(accuracy: float) -> ExifWriter`

设置位置精度（米）。

##### `set_creation_date(date_str: str, timezone_offset_hours: int = 8) -> ExifWriter`

设置创建日期/时间。

- `date_str`: 日期时间字符串，格式 "YYYY:MM:DD HH:MM:SS"（如 "2024:01:15 14:30:00"）
- `timezone_offset_hours`: 时区偏移小时数，用于 UTC 转换（默认 8，表示 UTC+8）

**注意**：
- 对于视频文件：创建日期会自动减去时区偏移转换为 UTC 时间写入 `CreateDate`、`MediaCreateDate`、`MediaModifyDate`，同时保留本地时间写入 `DateTimeOriginal`
- 对于图片文件：创建日期按原样写入，不进行时区转换

##### `set_timezone_offset(hours: int) -> ExifWriter`

设置时区偏移（用于视频文件的 UTC 转换）。

##### `write(filepath: str, dry_run: bool = False) -> Tuple[bool, str, str]`

写入 EXIF 元数据到文件。

- `filepath`: 文件路径
- `dry_run`: 如果为 True，只打印命令不执行

返回：`(success: bool, stdout: str, stderr: str)`

##### `write_batch(filepaths: List[str], dry_run: bool = False) -> List[Tuple[str, bool, str, str]]`

批量写入 EXIF 元数据到多个文件。

返回：每个文件的结果列表 `[(filepath, success, stdout, stderr), ...]`

##### `reset() -> ExifWriter`

重置所有参数为默认值。

## 时区处理说明

### 视频文件

视频文件（MP4, MOV 等）的 QuickTime/ISO 媒体时间戳使用 UTC 时间。因此：

- 输入的本地时间会自动减去时区偏移（默认 8 小时）转换为 UTC
- `CreateDate`、`MediaCreateDate`、`MediaModifyDate` 使用 UTC 时间
- `DateTimeOriginal` 保留本地时间（用于相册显示）

### 图片文件

图片文件的 EXIF 时间戳通常使用本地时间，因此：

- 输入的日期时间按原样写入，不进行时区转换
- `EXIF:DateTimeOriginal`、`EXIF:CreateDate`、`FileModifyDate` 都使用输入的本地时间

## 示例代码

更多示例请参考 `exif_writer_example.py` 文件。

## 错误处理

```python
from exif_writer import ExifWriter

writer = ExifWriter()

try:
    writer.set_gps(lat=34.673500, lon=112.492300)
    success, stdout, stderr = writer.write("video.mp4")
    
    if not success:
        print(f"写入失败: {stderr}")
except FileNotFoundError as e:
    print(f"文件未找到: {e}")
except ValueError as e:
    print(f"参数错误: {e}")
```

## 注意事项

1. 所有操作都会覆盖原始文件的元数据（使用 `-overwrite_original`）
2. 建议在重要文件上使用前先备份
3. 确保 exiftool 已正确安装并可用
4. GPS 坐标范围：纬度 -90 到 90，经度 -180 到 180
5. 日期格式必须严格遵循 "YYYY:MM:DD HH:MM:SS"

## 许可证

与主项目相同。

