"""
Performance monitoring utilities for the File Compressor application.
"""

import time
import psutil
import os
from typing import Dict, Any, Optional, Callable
from functools import wraps
from utils.logger import get_logger

logger = get_logger(__name__)

class PerformanceMonitor:
    """Monitor performance metrics during compression operations."""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {}
        self.start_time: Optional[float] = None
        self.start_memory: Optional[float] = None
    
    def start_monitoring(self, operation_name: str) -> None:
        """Start monitoring an operation."""
        self.start_time = time.time()
        self.start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        logger.info(f"Starting performance monitoring for: {operation_name}")
    
    def stop_monitoring(self, operation_name: str, file_path: str, 
                       original_size: float, compressed_size: Optional[float] = None) -> Dict[str, Any]:
        """Stop monitoring and return metrics."""
        if self.start_time is None:
            return {}
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        duration = end_time - self.start_time
        memory_used = end_memory - (self.start_memory or 0)
        
        metrics = {
            'operation': operation_name,
            'file_path': file_path,
            'duration_seconds': round(duration, 2),
            'memory_used_mb': round(memory_used, 2),
            'original_size_mb': round(original_size, 2),
            'compressed_size_mb': round(compressed_size, 2) if compressed_size else None,
            'compression_ratio': None
        }
        
        if compressed_size and original_size > 0:
            compression_ratio = (1 - compressed_size / original_size) * 100
            metrics['compression_ratio'] = round(compression_ratio, 1)
        
        self.metrics[operation_name] = metrics
        
        # Log performance metrics
        logger.info(f"Performance metrics for {operation_name}: "
                   f"Duration: {metrics['duration_seconds']}s, "
                   f"Memory: {metrics['memory_used_mb']}MB, "
                   f"Compression: {metrics['compression_ratio']}%")
        
        return metrics
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all monitored operations."""
        if not self.metrics:
            return {}
        
        total_duration = sum(m['duration_seconds'] for m in self.metrics.values())
        total_memory = sum(m['memory_used_mb'] for m in self.metrics.values())
        total_files = len(self.metrics)
        
        avg_compression_ratio = 0
        compression_ratios = [m['compression_ratio'] for m in self.metrics.values() 
                            if m['compression_ratio'] is not None]
        if compression_ratios:
            avg_compression_ratio = sum(compression_ratios) / len(compression_ratios)
        
        return {
            'total_files_processed': total_files,
            'total_duration_seconds': round(total_duration, 2),
            'total_memory_used_mb': round(total_memory, 2),
            'average_compression_ratio': round(avg_compression_ratio, 1),
            'average_duration_per_file': round(total_duration / total_files, 2) if total_files > 0 else 0
        }

def monitor_performance(operation_name: str):
    """Decorator to monitor performance of compression functions."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            monitor = PerformanceMonitor()
            
            # Extract file path from arguments
            file_path = args[0] if args else kwargs.get('file_path', 'unknown')
            
            # Get original file size
            original_size = 0
            try:
                if os.path.exists(file_path):
                    original_size = os.path.getsize(file_path) / 1024 / 1024  # MB
            except (OSError, TypeError):
                pass
            
            # Start monitoring
            monitor.start_monitoring(operation_name)
            
            try:
                # Execute the function
                result = func(*args, **kwargs)
                
                # Get compressed file size if result is a path
                compressed_size = None
                if result and isinstance(result, str) and os.path.exists(result):
                    try:
                        compressed_size = os.path.getsize(result) / 1024 / 1024  # MB
                    except OSError:
                        pass
                
                # Stop monitoring
                monitor.stop_monitoring(operation_name, file_path, original_size, compressed_size)
                
                return result
                
            except Exception as e:
                # Stop monitoring even if there's an error
                monitor.stop_monitoring(operation_name, file_path, original_size)
                raise e
        
        return wrapper
    return decorator

def get_system_info() -> Dict[str, Any]:
    """Get system information for performance analysis."""
    try:
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu_count': cpu_count,
            'memory_total_gb': round(memory.total / 1024 / 1024 / 1024, 2),
            'memory_available_gb': round(memory.available / 1024 / 1024 / 1024, 2),
            'memory_percent_used': round(memory.percent, 1),
            'disk_total_gb': round(disk.total / 1024 / 1024 / 1024, 2),
            'disk_free_gb': round(disk.free / 1024 / 1024 / 1024, 2),
            'disk_percent_used': round((disk.used / disk.total) * 100, 1)
        }
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return {}

def check_system_resources() -> Dict[str, bool]:
    """Check if system has sufficient resources for compression."""
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Check if we have at least 100MB free memory and 1GB free disk space
        memory_ok = memory.available > 100 * 1024 * 1024  # 100MB
        disk_ok = disk.free > 1024 * 1024 * 1024  # 1GB
        
        return {
            'memory_sufficient': memory_ok,
            'disk_sufficient': disk_ok,
            'system_ready': memory_ok and disk_ok
        }
    except Exception as e:
        logger.error(f"Error checking system resources: {e}")
        return {
            'memory_sufficient': False,
            'disk_sufficient': False,
            'system_ready': False
        }

# Global performance monitor instance
performance_monitor = PerformanceMonitor() 