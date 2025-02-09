from analytics.technical import TechnicalAnalyzer
from analytics.economic import EconomicAnalyzer
from analytics.environmental import EnvironmentalAnalyzer


class AnalysisService:
    def __init__(self):
        self.technical_analyzer = TechnicalAnalyzer()
        self.economic_analyzer = EconomicAnalyzer()
        self.environmental_analyzer = EnvironmentalAnalyzer()

    def perform_analysis(self, process_data):
        technical_results = self.technical_analyzer.analyze(
            process_data.technical_params
        )
        economic_results = self.economic_analyzer.analyze(
            process_data.economic_params
        )
        environmental_results = self.environmental_analyzer.analyze(
            process_data.environmental_params
        )

        return {
            'technical': technical_results,
            'economic': economic_results,
            'environmental': environmental_results
        }
