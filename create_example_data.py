#!/usr/bin/env python
"""Create example data for the Architecture CRUD application."""
import json
import os

example_data = {
    "adrs": {
        "ADR-001": {
            "id": "ADR-001",
            "title": "Use FastAPI for Backend",
            "status": "accepted",
            "date": "2024-01-15",
            "authors": ["John Smith", "Jane Doe"],
            "context": "We need to choose a web framework for our backend API that supports modern Python features, has good performance, and provides automatic API documentation.",
            "decision": "We will use FastAPI as our backend framework.",
            "alternatives": {
                "Flask": {
                    "advantages": ["Simple and lightweight", "Large ecosystem", "Well-documented"],
                    "disadvantages": ["No built-in async support", "Manual OpenAPI documentation", "Less type safety"]
                },
                "Django": {
                    "advantages": ["Full-featured", "Built-in admin", "ORM included"],
                    "disadvantages": ["Heavyweight for API-only apps", "Steeper learning curve", "Less suitable for microservices"]
                }
            },
            "relationships": {
                "qualities": [
                    {
                        "targetId": "QA-001",
                        "type": "addresses",
                        "strength": "strong"
                    }
                ],
                "risks": [
                    {
                        "targetId": "RISK-001",
                        "type": "accepts",
                        "strength": "medium"
                    }
                ],
                "technicalDebts": [],
                "components": [
                    {
                        "targetId": "COMP-001",
                        "type": "defines",
                        "strength": "strong"
                    }
                ],
                "relatedAdrs": []
            }
        },
        "ADR-002": {
            "id": "ADR-002",
            "title": "Use Streamlit for UI",
            "status": "accepted",
            "date": "2024-01-20",
            "authors": ["Jane Doe"],
            "context": "We need a rapid UI development framework that integrates well with Python and doesn't require extensive frontend knowledge.",
            "decision": "We will use Streamlit for the user interface.",
            "alternatives": {
                "React": {
                    "advantages": ["Highly flexible", "Large ecosystem", "Industry standard"],
                    "disadvantages": ["Requires separate frontend stack", "Longer development time", "Need JavaScript expertise"]
                },
                "Dash": {
                    "advantages": ["Python-based", "Good for data apps", "Plotly integration"],
                    "disadvantages": ["Steeper learning curve", "Less intuitive than Streamlit", "More complex layouts"]
                }
            },
            "relationships": {
                "qualities": [
                    {
                        "targetId": "QA-002",
                        "type": "addresses",
                        "strength": "strong"
                    }
                ],
                "risks": [],
                "technicalDebts": [
                    {
                        "targetId": "TD-001",
                        "type": "creates",
                        "strength": "medium"
                    }
                ],
                "components": [
                    {
                        "targetId": "COMP-002",
                        "type": "defines",
                        "strength": "strong"
                    }
                ],
                "relatedAdrs": []
            }
        }
    },
    "qualities": {
        "QA-001": {
            "id": "QA-001",
            "title": "High Performance",
            "description": "The system should respond to API requests within 200ms for 95% of requests under normal load.",
            "metrics": [
                {
                    "metricName": "Response Time",
                    "targetValue": "200",
                    "unit": "ms"
                },
                {
                    "metricName": "Throughput",
                    "targetValue": "1000",
                    "unit": "requests/second"
                }
            ],
            "priority": "must"
        },
        "QA-002": {
            "id": "QA-002",
            "title": "Rapid Development",
            "description": "New features should be implementable within days, not weeks. The UI should be easy to modify and extend.",
            "metrics": [
                {
                    "metricName": "Feature Development Time",
                    "targetValue": "3",
                    "unit": "days"
                }
            ],
            "priority": "should"
        },
        "QA-003": {
            "id": "QA-003",
            "title": "Security",
            "description": "The system must protect against common web vulnerabilities and ensure data integrity.",
            "metrics": [
                {
                    "metricName": "Security Score",
                    "targetValue": "A",
                    "unit": "grade"
                }
            ],
            "priority": "must"
        }
    },
    "risks": {
        "RISK-001": {
            "id": "RISK-001",
            "title": "Limited FastAPI Expertise",
            "description": "The team has limited experience with FastAPI, which may lead to implementation challenges.",
            "impact": "medium",
            "likelihood": "high",
            "mitigationStrategy": "Provide team training, establish code review process, create coding standards",
            "status": "identified"
        },
        "RISK-002": {
            "id": "RISK-002",
            "title": "Streamlit Scalability",
            "description": "Streamlit may not scale well for large numbers of concurrent users.",
            "impact": "high",
            "likelihood": "medium",
            "mitigationStrategy": "Monitor usage patterns, implement caching, consider alternative UI if needed",
            "status": "monitoring"
        }
    },
    "technicalDebts": {
        "TD-001": {
            "id": "TD-001",
            "title": "Limited UI Customization",
            "description": "Streamlit provides limited customization options compared to traditional web frameworks.",
            "impact": "medium",
            "effort": "high",
            "remediationPlan": "If custom UI requirements increase, migrate to React-based frontend",
            "status": "identified"
        },
        "TD-002": {
            "id": "TD-002",
            "title": "JSON File Storage",
            "description": "Using JSON files for data storage limits scalability and concurrent access.",
            "impact": "high",
            "effort": "medium",
            "remediationPlan": "Implement database backend (PostgreSQL) when user base grows",
            "status": "backlog"
        }
    },
    "components": {
        "COMP-001": {
            "id": "COMP-001",
            "title": "API Backend",
            "responsibility": "Handle all business logic, data validation, and persistence",
            "interfaces": [
                "REST API endpoints",
                "OpenAPI documentation",
                "JSON data format"
            ],
            "attributes": {
                "framework": "FastAPI",
                "language": "Python 3.11",
                "deployment": "Docker container"
            }
        },
        "COMP-002": {
            "id": "COMP-002",
            "title": "Web UI",
            "responsibility": "Provide user interface for CRUD operations and data visualization",
            "interfaces": [
                "HTTP client to API",
                "Web browser interface"
            ],
            "attributes": {
                "framework": "Streamlit",
                "language": "Python 3.11",
                "deployment": "Docker container"
            }
        },
        "COMP-003": {
            "id": "COMP-003",
            "title": "Data Layer",
            "responsibility": "Manage data persistence and validation",
            "interfaces": [
                "Repository pattern",
                "JSON schema validation"
            ],
            "attributes": {
                "storage": "JSON files",
                "validation": "Pydantic models"
            }
        }
    }
}

if __name__ == "__main__":
    output_path = "data/example_architecture.json"
    os.makedirs("data", exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(example_data, f, indent=2)
    
    print(f"Example data created at {output_path}")
