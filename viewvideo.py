import streamlit as st
import os
import glob
from pathlib import Path

# 页面配置
st.set_page_config(page_title="本地视频浏览器", page_icon="🎬", layout="wide")

# 自定义CSS样式
st.markdown("""
    <style>
    .video-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    .delete-btn {
        background-color: #ff4b4b;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }
    .delete-btn:hover {
        background-color: #ff3333;
    }
    </style>
""", unsafe_allow_html=True)

# 标题
st.title("🎬 本地视频浏览器")

# 侧边栏 - 视频目录选择
st.sidebar.header("设置")
video_directory = st.sidebar.text_input(
    "视频文件夹路径",
    value=os.getcwd(),
    help="输入包含视频的文件夹路径"
)

# 支持的视频格式
VIDEO_EXTENSIONS = ['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm', 'm4v']


def get_video_files(directory):
    """获取目录下所有视频文件"""
    video_files = []
    for ext in VIDEO_EXTENSIONS:
        video_files.extend(glob.glob(os.path.join(directory, f'*.{ext}')))
        video_files.extend(glob.glob(os.path.join(directory, f'*.{ext.upper()}')))
    return sorted(video_files)


def format_file_size(file_path):
    """格式化文件大小"""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


# 检查目录是否存在
if not os.path.exists(video_directory):
    st.error(f"❌ 目录不存在: {video_directory}")
    st.stop()

# 获取视频列表
video_files = get_video_files(video_directory)

if not video_files:
    st.warning(f"⚠️ 在目录 '{video_directory}' 中未找到视频文件")
    st.info(f"支持的视频格式: {', '.join(VIDEO_EXTENSIONS)}")
    st.stop()

# 显示统计信息
st.sidebar.success(f"✅ 找到 {len(video_files)} 个视频文件")

# 会话状态初始化
if 'current_video_index' not in st.session_state:
    st.session_state.current_video_index = 0

if 'confirm_delete' not in st.session_state:
    st.session_state.confirm_delete = False

# 确保索引在有效范围内
if st.session_state.current_video_index >= len(video_files):
    st.session_state.current_video_index = 0

# 当前视频
current_video_path = video_files[st.session_state.current_video_index]
current_video_name = os.path.basename(current_video_path)

# 显示当前视频信息
st.header(f"📹 {current_video_name}")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.info(f"文件大小: {format_file_size(current_video_path)}")

# 视频播放器
video_file = open(current_video_path, 'rb')
video_bytes = video_file.read()
st.video(video_bytes)
video_file.close()

# 控制按钮
st.markdown("---")
col_prev, col_center, col_next, col_delete = st.columns([1, 1, 1, 1])

with col_prev:
    if st.button("⏮️ 上一个", key="prev_btn", use_container_width=True):
        st.session_state.current_video_index = (st.session_state.current_video_index - 1) % len(video_files)
        st.session_state.confirm_delete = False
        st.rerun()

with col_next:
    if st.button("⏭️ 下一个", key="next_btn", use_container_width=True):
        st.session_state.current_video_index = (st.session_state.current_video_index + 1) % len(video_files)
        st.session_state.confirm_delete = False
        st.rerun()

with col_delete:
    if not st.session_state.confirm_delete:
        if st.button("🗑️ 删除视频", key="delete_btn", use_container_width=True):
            st.session_state.confirm_delete = True
            st.rerun()
    else:
        st.warning("⚠️ 确认删除？")
        col_confirm, col_cancel = st.columns(2)
        with col_confirm:
            if st.button("✅ 确认删除", key="confirm_btn", use_container_width=True, type="primary"):
                try:
                    os.remove(current_video_path)
                    st.success(f"✅ 已删除: {current_video_name}")

                    # 重新获取视频列表
                    video_files = get_video_files(video_directory)

                    if not video_files:
                        st.warning("所有视频已被删除")
                        st.session_state.current_video_index = 0
                        st.session_state.confirm_delete = False
                        st.rerun()

                    # 调整索引
                    if st.session_state.current_video_index >= len(video_files):
                        st.session_state.current_video_index = 0

                    st.session_state.confirm_delete = False
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 删除失败: {str(e)}")
        with col_cancel:
            if st.button("❌ 取消", key="cancel_btn", use_container_width=True):
                st.session_state.confirm_delete = False
                st.rerun()

# 视频列表
st.markdown("---")
st.subheader(f"📋 视频列表 (共 {len(video_files)} 个)")

# 显示视频列表
for idx, video_path in enumerate(video_files):
    video_name = os.path.basename(video_path)
    file_size = format_file_size(video_path)

    # 高亮当前视频
    if idx == st.session_state.current_video_index:
        st.markdown(f"**▶️ {idx + 1}. {video_name}** ({file_size}) - *当前播放*")
    else:
        if st.button(f"{idx + 1}. {video_name} ({file_size})", key=f"select_{idx}", use_container_width=True):
            st.session_state.current_video_index = idx
            st.session_state.confirm_delete = False
            st.rerun()

# 页脚
st.markdown("---")
st.caption("💡 提示: 使用'上一个'和'下一个'按钮切换视频，点击'删除视频'可删除当前视频")


