try:
    from .app import main
except ImportError:
    from vehicle_data_generator.app import main


if __name__ == "__main__":
    raise SystemExit(main())
