import os
import json
from pathlib import Path
from typing import Dict, List

class ReportGenerator:
    def __init__(self, config: dict):
        self.config = config
        self.report_dir = Path(config["execution"]["report_dir"])
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, feature: Dict, execution_result: Dict) -> Path:
        """
        Generate report in configured format
        """
        report_name = f"{feature['name'].replace(' ', '_')}_report"
        if self.config["reporting"]["format"] == "html":
            report_path = self._generate_html(feature, execution_result, report_name)
        elif self.config["reporting"]["format"] == "pdf":
            report_path = self._generate_pdf(feature, execution_result, report_name)
        else:  # json
            report_path = self._generate_json(feature, execution_result, report_name)

        return report_path

    def _generate_html(self, feature: Dict, execution_result: Dict, report_name: str) -> Path:
        """
        Generate HTML report with screenshots and videos
        """
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{feature['name']} Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .passed {{ color: green; }}
                .failed {{ color: red; }}
                .scenario {{ margin-bottom: 20px; padding: 10px; border: 1px solid #ccc; }}
                .screenshot {{ max-width: 300px; margin: 5px; }}
                .video {{ max-width: 600px; margin: 5px; }}
            </style>
        </head>
        <body>
            <h1>{feature['name']} Report</h1>
            <p>Status: <span class="{execution_result['status']}">{execution_result['status'].upper()}</span></p>
            <p>Duration: {execution_result['duration']:.2f} seconds</p>
            <h2>Scenarios</h2>
        """

        for scenario in feature["scenarios"]:
            html_content += f"""
            <div class="scenario">
                <h3>{scenario['name']}</h3>
                <p>Given: {', '.join(scenario['given'])}</p>
                <p>When: {', '.join(scenario['when'])}</p>
                <p>Then: {', '.join(scenario['then'])}</p>
            </div>
            """

        # Add screenshots if any
        if execution_result.get("screenshots"):
            html_content += "<h2>Screenshots on Failure</h2>"
            for screenshot in execution_result["screenshots"]:
                html_content += f'<img src="{screenshot}" class="screenshot" alt="Screenshot">'

        # Add videos if any
        if execution_result.get("videos"):
            html_content += "<h2>Test Videos</h2>"
            for video in execution_result["videos"]:
                html_content += f'<video controls class="video"><source src="{video}" type="video/mp4"></video>'

        html_content += """
        </body>
        </html>
        """

        report_path = self.report_dir / f"{report_name}.html"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return report_path

    def _generate_pdf(self, feature: Dict, execution_result: Dict, report_name: str) -> Path:
        """
        Generate PDF report (placeholder — use weasyprint or similar in real code)
        """
        report_path = self.report_dir / f"{report_name}.pdf"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"PDF report for {feature['name']} - Status: {execution_result['status']}")
        return report_path

    def _generate_json(self, feature: Dict, execution_result: Dict, report_name: str) -> Path:
        """
        Generate JSON report
        """
        report_data = {
            "feature": feature["name"],
            "status": execution_result["status"],
            "duration": execution_result["duration"],
            "scenarios": feature["scenarios"],
            "errors": execution_result.get("errors", []),
            "screenshots": execution_result.get("screenshots", []),
            "videos": execution_result.get("videos", [])
        }

        report_path = self.report_dir / f"{report_name}.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        return report_path