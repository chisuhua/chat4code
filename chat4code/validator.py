"""
chat4code 响应验证模块
"""

from .parser import ResponseParser
import re

class ResponseValidator:
    def __init__(self):
        self.parser = ResponseParser()

    def validate(self, markdown_content: str, verbose: bool = False) -> dict:
        """
        验证AI响应格式是否正确
        """
        result = {
            'is_valid': False,
            'issues': [],
            'warnings': [],
            'file_count': 0,
            'files': [],
            'format_type': 'unknown'
        }
        
        try:
            # 尝试标准格式提取
            standard_files = self.parser.extract_files_standard(markdown_content)
            if standard_files:
                result['format_type'] = 'standard'
                result['file_count'] = len(standard_files)
                result['files'] = [f[0] for f in standard_files]
                result['is_valid'] = True
                
                if verbose:
                    result['details'] = {
                        'extracted_files': standard_files,
                        'method': 'standard_parsing'
                    }
                return result
            
            # 尝试灵活格式提取
            flexible_files = self.parser.extract_files_flexible(markdown_content)
            if flexible_files:
                result['format_type'] = 'flexible'
                result['file_count'] = len(flexible_files)
                result['files'] = [f[0] for f in flexible_files]
                result['is_valid'] = True
                result['warnings'].append("使用了灵活解析模式，建议使用标准格式")
                
                if verbose:
                    result['details'] = {
                        'extracted_files': flexible_files,
                        'method': 'flexible_parsing'
                    }
                return result
            
            # 没有找到文件
            result['issues'].append("未找到有效的文件格式")
            result['format_type'] = 'none'
            
            # 检查是否有代码块但没有正确格式
            code_blocks = re.findall(r'```(\w*)\n(.*?)\n\s*```', markdown_content, re.DOTALL)
            if code_blocks:
                result['warnings'].append(f"发现 {len(code_blocks)} 个代码块，但格式不符合要求")
                result['format_type'] = 'code_blocks_only'
                
        except Exception as e:
            result['issues'].append(f"解析错误: {str(e)}")
        
        return result

    def validate_with_suggestions(self, markdown_content: str) -> dict:
        """
        验证并提供改进建议
        """
        result = self.validate(markdown_content)
        
        if not result['is_valid']:
            suggestions = self._generate_fix_suggestions(markdown_content)
            result['suggestions'] = suggestions
        
        return result

    def _generate_fix_suggestions(self, content: str) -> list[str]:
        """生成修复建议"""
        suggestions = []
        
        # 检查常见的格式问题
        if '##' not in content:
            suggestions.append("未找到文件标题标记，请使用 ## 文件路径 格式")
        
        if '```' not in content:
            suggestions.append("未找到代码块标记，请使用 ```language 格式")
        
        # 检查文件路径格式
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('##'):
                file_path = line.strip()[2:].strip()
                if not self.parser._is_valid_file_path(file_path):
                    suggestions.append(f"文件路径 '{file_path}' 格式可能不正确")
        
        return suggestions
