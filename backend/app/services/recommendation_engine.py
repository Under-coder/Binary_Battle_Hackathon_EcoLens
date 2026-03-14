def get_restoration_plan(cause):
    """Return restoration recommendations based on predicted cause."""
    cause_lower = cause.lower()
    if "deforestation" in cause_lower or "urban expansion" in cause_lower:
        recommendations = [
            "Launch afforestation programs",
            "Protect existing forest areas",
            "Introduce urban green belts"
        ]
    elif "drought" in cause_lower:
        recommendations = [
            "Implement rainwater harvesting",
            "Improve water conservation systems",
            "Promote drought-resistant vegetation"
        ]
    elif "soil degradation" in cause_lower:
        recommendations = [
            "Adopt soil restoration techniques",
            "Encourage sustainable agriculture",
            "Reduce chemical fertilizer use"
        ]
    else:
        recommendations = [
            "Maintain conservation policies",
            "Monitor vegetation health regularly"
        ]
    return recommendations


def estimate_recovery_time(vegetation_status):
    """Return rough recovery estimate based on vegetation health."""
    if vegetation_status == "Degraded Vegetation":
        return "Estimated recovery time: 6–10 years with active restoration"
    elif vegetation_status == "Moderate Vegetation":
        return "Estimated recovery time: 3–5 years with conservation efforts"
    elif vegetation_status == "Healthy Vegetation":
        return "Ecosystem is currently stable"
    else:
        return "Recovery time cannot be determined"