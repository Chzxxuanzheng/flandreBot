import os
from pathlib import Path
from typing import Optional, ClassVar
from nonebot import logger


class ProcessLock:
	"""简单的基于PID文件的进程锁"""
	
	_lock_file: ClassVar[Optional[Path]] = None
	_current_pid: ClassVar[Optional[int]] = None
	
	@classmethod
	def _ensure_initialized(cls, lock_file: str = "bot.lock"):
		"""确保类已初始化"""
		if cls._lock_file is None:
			cls._lock_file = Path(lock_file)
		if cls._current_pid is None:
			cls._current_pid = os.getpid()
	
	@classmethod
	def _is_process_running(cls, pid: int) -> bool:
		"""检查指定PID的进程是否正在运行"""
		try:
			# 发送信号0不会实际发送信号，只是检查进程是否存在
			os.kill(pid, 0)
			return True
		except (OSError, ProcessLookupError):
			return False
	
	@classmethod
	def _read_pid(cls) -> Optional[int]:
		"""从锁文件读取PID"""
		try:
			if cls._lock_file and cls._lock_file.exists():
				content = cls._lock_file.read_text().strip()
				if content:
					return int(content)
		except (ValueError, FileNotFoundError):
			pass
		return None
	
	@classmethod
	def _write_pid(cls):
		"""将当前PID写入锁文件"""
		if cls._lock_file and cls._current_pid:
			cls._lock_file.write_text(str(cls._current_pid))
	
	@classmethod
	def _remove_lock(cls):
		"""删除锁文件"""
		try:
			if cls._lock_file and cls._lock_file.exists():
				cls._lock_file.unlink()
		except FileNotFoundError:
			pass
	
	@classmethod
	def acquire(cls, lock_file: str = "bot.lock") -> bool:
		"""获取锁，返回是否成功"""
		cls._ensure_initialized(lock_file)
		existing_pid = cls._read_pid()
		
		if existing_pid is not None:
			if cls._is_process_running(existing_pid):
				logger.opt(colors=True).error(
					f"进程锁已存在 (PID: <y>{existing_pid}</y>)，可能有其他实例正在运行"
				)
				return False
			else:
				logger.opt(colors=True).warning(
					f"上次未正常退出"
				)
				cls._remove_lock()

		# 写入当前PID
		cls._write_pid()
		return True
	
	@classmethod
	def release(cls):
		"""释放锁"""
		# 检查锁文件中的PID是否是当前进程
		existing_pid = cls._read_pid()
		if existing_pid == cls._current_pid:
			cls._remove_lock()
			logger.success('退出成功')
		else:
			logger.warning(f"警告: 锁文件PID ({existing_pid}) 与当前进程PID ({cls._current_pid}) 不匹配")

	def __init__(self, lock_file: str = "bot.lock"):
		"""锁管理器"""
		self.lock_file_path = lock_file
	
	def __enter__(self):
		"""上下文管理器入口"""
		if not ProcessLock.acquire(self.lock_file_path):
			raise RuntimeError("获取锁失败")
		return self
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		"""上下文管理器出口，自动释放锁"""
		ProcessLock.release()