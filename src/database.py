"""
Класс работы с базой данных.
Использует SQLite для хранения результатов вычислений.
"""

import sqlite3
from typing import Optional, Dict, Any


class Database:
    """Класс для работы с базой данных SQLite."""

    def __init__(self, db_path: str = ":memory:"):
        """
        Инициализация подключения к БД.

        Args:
            db_path: Путь к файлу БД. По умолчанию — в памяти.
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self) -> None:
        """Создание таблицы для хранения результатов вычислений скидок."""
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS discount_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                is_vip INTEGER NOT NULL,
                result REAL NOT NULL,
                error_message TEXT
            )
        """)
        self.connection.commit()

    def add_record(self, price: float, quantity: int, is_vip: bool,
                   result: float, error_message: Optional[str] = None) -> int:
        """
        Добавление записи в БД.

        Args:
            price: Цена товара.
            quantity: Количество товара.
            is_vip: Признак VIP-клиента.
            result: Результат вычисления.
            error_message: Сообщение об ошибке (если есть).

        Returns:
            ID добавленной записи.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO discount_results (price, quantity, is_vip, result, error_message)
            VALUES (?, ?, ?, ?, ?)
        """, (price, quantity, int(is_vip), result, error_message))
        self.connection.commit()
        return cursor.lastrowid

    def get_record(self, price: float, quantity: int, is_vip: bool) -> Optional[Dict[str, Any]]:
        """
        Получение записи из БД по параметрам.

        Args:
            price: Цена товара.
            quantity: Количество товара.
            is_vip: Признак VIP-клиента.

        Returns:
            Словарь с данными записи или None, если запись не найдена.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, price, quantity, is_vip, result, error_message
            FROM discount_results
            WHERE price = ? AND quantity = ? AND is_vip = ?
        """, (price, quantity, int(is_vip)))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "price": row[1],
                "quantity": row[2],
                "is_vip": bool(row[3]),
                "result": row[4],
                "error_message": row[5]
            }
        return None

    def delete_record(self, record_id: int) -> bool:
        """
        Удаление записи из БД по ID.

        Args:
            record_id: ID записи для удаления.

        Returns:
            True, если запись удалена, False если не найдена.
        """
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM discount_results WHERE id = ?", (record_id,))
        self.connection.commit()
        return cursor.rowcount > 0

    def close(self) -> None:
        """Закрытие подключения к БД."""
        self.connection.close()

    def __del__(self):
        """Деструктор — закрывает соединение при удалении объекта."""
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
