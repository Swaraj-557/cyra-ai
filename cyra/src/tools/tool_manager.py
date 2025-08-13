"""
Tool Manager - Coordinate and execute cybersecurity tools
"""
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Callable
from src.tools.password_generator import PasswordGenerator

logger = logging.getLogger(__name__)


class ToolManager:
    """Manage and execute cybersecurity tools through natural language interface"""
    
    def __init__(self):
        self.password_generator = PasswordGenerator()
        self.tools: Dict[str, Callable] = {
            "generate_password": self._generate_password,
            "assess_password_strength": self._assess_password_strength,
            "generate_passphrase": self._generate_passphrase,
            "check_password_breach": self._check_password_breach,
            "scan_network": self._scan_network,
            "port_scan": self._port_scan,
            "get_security_advice": self._get_security_advice,
        }
    
    def get_openai_tools(self) -> List[Dict[str, Any]]:
        """
        Get tool definitions for OpenAI function calling
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "generate_password",
                    "description": "Generate a secure password with customizable options",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "length": {
                                "type": "integer",
                                "description": "Password length (4-128 characters)",
                                "default": 16
                            },
                            "include_uppercase": {
                                "type": "boolean",
                                "description": "Include uppercase letters",
                                "default": True
                            },
                            "include_lowercase": {
                                "type": "boolean",
                                "description": "Include lowercase letters",
                                "default": True
                            },
                            "include_digits": {
                                "type": "boolean",
                                "description": "Include numbers",
                                "default": True
                            },
                            "include_special": {
                                "type": "boolean",
                                "description": "Include special characters",
                                "default": True
                            },
                            "exclude_ambiguous": {
                                "type": "boolean",
                                "description": "Exclude ambiguous characters (0, O, 1, l, I)",
                                "default": False
                            },
                            "count": {
                                "type": "integer",
                                "description": "Number of passwords to generate",
                                "default": 1
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "assess_password_strength",
                    "description": "Analyze the strength and security of a password",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "password": {
                                "type": "string",
                                "description": "The password to analyze"
                            }
                        },
                        "required": ["password"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_passphrase",
                    "description": "Generate a memorable passphrase using common words",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "word_count": {
                                "type": "integer",
                                "description": "Number of words in the passphrase",
                                "default": 4
                            },
                            "separator": {
                                "type": "string",
                                "description": "Character to separate words",
                                "default": "-"
                            },
                            "include_numbers": {
                                "type": "boolean",
                                "description": "Add random numbers to the passphrase",
                                "default": True
                            },
                            "capitalize": {
                                "type": "boolean",
                                "description": "Capitalize first letter of each word",
                                "default": True
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_password_breach",
                    "description": "Check if a password contains patterns commonly found in data breaches",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "password": {
                                "type": "string",
                                "description": "The password to check for breach patterns"
                            }
                        },
                        "required": ["password"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "scan_network",
                    "description": "Perform network discovery scan to find active hosts",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "target": {
                                "type": "string",
                                "description": "Target network or IP range (e.g., 192.168.1.0/24)"
                            },
                            "scan_type": {
                                "type": "string",
                                "description": "Type of scan to perform",
                                "enum": ["ping", "quick", "comprehensive"],
                                "default": "ping"
                            }
                        },
                        "required": ["target"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "port_scan",
                    "description": "Scan specific ports on a target host",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "target": {
                                "type": "string",
                                "description": "Target IP address or hostname"
                            },
                            "ports": {
                                "type": "string",
                                "description": "Port range or specific ports (e.g., '80,443,22' or '1-1000')",
                                "default": "1-1000"
                            },
                            "scan_type": {
                                "type": "string",
                                "description": "Type of port scan",
                                "enum": ["tcp", "udp", "syn"],
                                "default": "tcp"
                            }
                        },
                        "required": ["target"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_security_advice",
                    "description": "Get cybersecurity advice and best practices on a specific topic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "The security topic to get advice about"
                            },
                            "context": {
                                "type": "string",
                                "description": "Additional context about the user's situation",
                                "default": ""
                            }
                        },
                        "required": ["topic"]
                    }
                }
            }
        ]
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Execute a specific tool with given parameters
        """
        logger.info(f"Executing tool '{tool_name}' for user {user_id} with parameters: {parameters}")
        
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found",
                "available_tools": list(self.tools.keys())
            }
        
        try:
            result = await self.tools[tool_name](**parameters)
            return {
                "success": True,
                "tool": tool_name,
                "result": result,
                "user_id": user_id
            }
        except Exception as e:
            logger.error(f"Error executing tool '{tool_name}': {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name
            }
    
    async def _generate_password(self, **kwargs) -> Dict[str, Any]:
        """Generate secure password(s)"""
        try:
            count = kwargs.pop('count', 1)
            
            if count == 1:
                password = self.password_generator.generate_password(**kwargs)
                strength = self.password_generator.assess_password_strength(password)
                return {
                    "password": password,
                    "strength": {
                        "score": strength.score,
                        "level": strength.level,
                        "feedback": strength.feedback,
                        "crack_time": strength.estimated_crack_time
                    }
                }
            else:
                passwords = self.password_generator.generate_multiple_passwords(count, **kwargs)
                results = []
                for pwd in passwords:
                    strength = self.password_generator.assess_password_strength(pwd)
                    results.append({
                        "password": pwd,
                        "strength_score": strength.score,
                        "strength_level": strength.level
                    })
                return {"passwords": results}
                
        except Exception as e:
            return {"error": str(e)}
    
    async def _assess_password_strength(self, password: str) -> Dict[str, Any]:
        """Assess password strength"""
        try:
            strength = self.password_generator.assess_password_strength(password)
            return {
                "score": strength.score,
                "level": strength.level,
                "feedback": strength.feedback,
                "estimated_crack_time": strength.estimated_crack_time
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _generate_passphrase(self, **kwargs) -> Dict[str, Any]:
        """Generate memorable passphrase"""
        try:
            passphrase = self.password_generator.generate_passphrase(**kwargs)
            strength = self.password_generator.assess_password_strength(passphrase)
            return {
                "passphrase": passphrase,
                "strength": {
                    "score": strength.score,
                    "level": strength.level,
                    "estimated_crack_time": strength.estimated_crack_time
                }
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _check_password_breach(self, password: str) -> Dict[str, Any]:
        """Check password for breach patterns"""
        try:
            warnings = self.password_generator.check_breach_patterns(password)
            return {
                "warnings": warnings,
                "is_potentially_compromised": len(warnings) > 0,
                "recommendation": "Consider using a different password" if warnings else "Password looks good"
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _scan_network(self, target: str, scan_type: str = "ping") -> Dict[str, Any]:
        """Perform network scan (placeholder - requires nmap installation)"""
        # Note: This is a placeholder implementation
        # In production, you would use python-nmap or subprocess to run nmap
        logger.warning("Network scanning not fully implemented - requires nmap installation")
        
        return {
            "target": target,
            "scan_type": scan_type,
            "status": "placeholder_implementation",
            "message": "Network scanning requires nmap to be installed and configured",
            "recommendation": "Install nmap and update this implementation for full functionality"
        }
    
    async def _port_scan(self, target: str, ports: str = "1-1000", scan_type: str = "tcp") -> Dict[str, Any]:
        """Perform port scan (placeholder - requires nmap installation)"""
        # Note: This is a placeholder implementation
        logger.warning("Port scanning not fully implemented - requires nmap installation")
        
        return {
            "target": target,
            "ports": ports,
            "scan_type": scan_type,
            "status": "placeholder_implementation",
            "message": "Port scanning requires nmap to be installed and configured",
            "recommendation": "Install nmap and update this implementation for full functionality"
        }
    
    async def _get_security_advice(self, topic: str, context: str = "") -> Dict[str, Any]:
        """Provide security advice"""
        # This could be enhanced with a knowledge base or external APIs
        advice_db = {
            "password": {
                "summary": "Use strong, unique passwords for every account",
                "best_practices": [
                    "Use passwords at least 12 characters long",
                    "Include uppercase, lowercase, numbers, and special characters",
                    "Avoid personal information and common words",
                    "Use a password manager to generate and store passwords",
                    "Enable two-factor authentication when available"
                ],
                "common_mistakes": [
                    "Reusing passwords across multiple accounts",
                    "Using predictable patterns or keyboard walks",
                    "Storing passwords in plain text",
                    "Using personal information in passwords"
                ]
            },
            "phishing": {
                "summary": "Phishing attacks try to steal credentials through deceptive emails and websites",
                "best_practices": [
                    "Verify sender identity before clicking links",
                    "Check URLs carefully for misspellings or suspicious domains",
                    "Use bookmarks for important sites instead of clicking email links",
                    "Enable email filtering and anti-phishing tools",
                    "Report suspicious emails to your IT department"
                ],
                "warning_signs": [
                    "Urgent or threatening language",
                    "Requests for sensitive information via email",
                    "Suspicious links or attachments",
                    "Generic greetings instead of your name",
                    "Poor grammar or spelling"
                ]
            },
            "wifi": {
                "summary": "Secure your wireless networks and be cautious on public WiFi",
                "best_practices": [
                    "Use WPA3 encryption (or WPA2 if WPA3 unavailable)",
                    "Change default router passwords",
                    "Use strong WiFi passwords",
                    "Keep router firmware updated",
                    "Disable WPS if not needed",
                    "Use a VPN on public WiFi"
                ],
                "risks": [
                    "Man-in-the-middle attacks on public WiFi",
                    "Weak encryption allows eavesdropping",
                    "Default credentials provide easy access",
                    "Outdated firmware may have vulnerabilities"
                ]
            }
        }
        
        topic_lower = topic.lower()
        advice = None
        
        # Find matching advice
        for key, value in advice_db.items():
            if key in topic_lower:
                advice = value
                break
        
        if not advice:
            advice = {
                "summary": f"General security advice for {topic}",
                "best_practices": [
                    "Keep software and systems updated",
                    "Use strong authentication methods",
                    "Follow the principle of least privilege",
                    "Implement defense in depth strategies",
                    "Regular security training and awareness"
                ],
                "recommendation": "For specific advice, please provide more details about your security concern"
            }
        
        return {
            "topic": topic,
            "context": context,
            "advice": advice
        }
    
    def get_tool_list(self) -> List[str]:
        """Get list of available tools"""
        return list(self.tools.keys())
