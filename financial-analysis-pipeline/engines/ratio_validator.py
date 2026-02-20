def validate_ratios(metrics: dict, company: str, year: int):

    def out_of_bounds(value, lower, upper):
        return value is not None and not (lower <= value <= upper)

    if out_of_bounds(metrics.get("operating_margin"), -1, 1):
        raise ValueError(
            f"{company} {year}: Operating margin outside logical bounds."
        )

    if out_of_bounds(metrics.get("gross_margin"), -1, 1):
        raise ValueError(
            f"{company} {year}: Gross margin outside logical bounds."
        )

    if metrics.get("current_ratio") is not None and metrics["current_ratio"] < 0:
        raise ValueError(
            f"{company} {year}: Current ratio cannot be negative."
        )

    return metrics
