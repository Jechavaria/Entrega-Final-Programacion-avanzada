from db import init_db, save_metrics
from model import train_and_save_model


def main():
    init_db()
    metrics = train_and_save_model()
    save_metrics(metrics)
    print("Entrenamiento completado")
    print(metrics)


if __name__ == "__main__":
    main()
