from celery import shared_task
from .models import ProcessAnalysis
from analytics.technical import perform_technical_analysis
from analytics.economic import perform_economic_analysis
from analytics.environmental import perform_environmental_analysis


@shared_task
def analyze_process(process_id: int):
    process = ProcessAnalysis.objects.get(id=process_id)
    try:
        process.status = 'processing'
        process.save()

        # Technical Analysis
        process.progress = 25
        process.save()
        technical_results = perform_technical_analysis(
            process.technical_params)
        process.technical_results = technical_results

        # Economic Analysis
        process.progress = 50
        process.save()
        economic_results = perform_economic_analysis(process.economic_params)
        process.economic_results = economic_results

        # Environmental Analysis
        process.progress = 75
        process.save()
        environmental_results = perform_environmental_analysis(
            process.environmental_params)
        process.environmental_results = environmental_results

        process.status = 'completed'
        process.progress = 100
        process.save()

    except Exception as e:
        process.status = 'failed'
        process.error_message = str(e)
        process.save()
        raise
