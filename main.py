import ui
import beaupy as bp

def main():
    ui.show()
    ui.contrib()
    url = bp.prompt(
        prompt="\n[white]Enter the URL of the target you want to flood: ",
        target_type=str,
        validator=lambda input: len(input) > 0,
        secure=False,
        raise_validation_fail=True,
        raise_type_conversion_fail=True,
        initial_value=None,
        completion=None
    )

if __name__ == "__main__":
    main()
    