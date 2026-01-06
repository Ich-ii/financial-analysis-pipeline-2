# engines/schema_validator.py

from engines.engine_interfaces import ENGINE_SCHEMAS

def validate_engine_output(output: list, engine_name: str):
    if engine_name not in ENGINE_SCHEMAS:
        raise ValueError(f"Unknown engine: {engine_name}")

    schema = ENGINE_SCHEMAS[engine_name]
    required_keys = schema.get("required_keys", set())

    for i, row in enumerate(output):
        row_keys = set(row.keys())

        # 1. Validate top-level required keys
        missing = required_keys - row_keys
        if missing:
            raise ValueError(
                f"{engine_name} output row {i} missing required keys: {missing}"
            )

        # 2. Validate metrics block (if defined)
        if "metrics" in schema:
            metrics_required = schema["metrics"]
            metrics_present = set(row.get("metrics", {}).keys())

            missing_metrics = metrics_required - metrics_present
            if missing_metrics:
                raise ValueError(
                    f"{engine_name} output row {i} missing metrics: {missing_metrics}"
                )

        # 3. Validate flags block (if defined)
        if "flags" in schema:
            flags_required = schema["flags"]
            flags_present = set(row.get("flags", {}).keys())

            missing_flags = flags_required - flags_present
            if missing_flags:
                raise ValueError(
                    f"{engine_name} output row {i} missing flags: {missing_flags}"
                )

    print(f"✅ {engine_name} output validated successfully.")
