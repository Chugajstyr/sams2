/***************************************************************************
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/
#ifndef DBCLEANER_H
#define DBCLEANER_H

using namespace std;

#include <string>

class SamsConfig;
class UserFilter;
class DateFilter;

/**
 * @brief Очистка таблиц кэша и счетчиков пользователей
 */
class DBCleaner
{
public:
  /**
   * @brief Конструктор
   *
   * @param proxyid Идентификатор прокси
   */
  DBCleaner (int proxyid);

  /**
   * @brief Деструктор
   */
   ~DBCleaner ();

  /**
   * @brief Устанавливает фильтр по пользователям
   *
   * @param filt Фильтр пользователей
   */
  void setUserFilter (UserFilter * filt);

  /**
   * @brief Устанавливает фильтр по датам
   *
   * @param filt Фильтр по датам
   */
  void setDateFilter (DateFilter * filt);

  /**
   * @brief Очищает счетчики пользователей
   */
  void clearCounters ();

  /**
   * @brief Очищает кэш протоколов доступа squid
   */
  void clearCache ();

protected:
    string _datasource;         ///< Источник данных ODBC
  string _user;                 ///< Имя пользователя для подключения к БД
  string _pass;                 ///< Пароль для подключения к БД
  int _proxyid;                 ///< Идентификатор прокси
  DateFilter *_date_filter;     ///< Текущий фильтр по датам
  UserFilter *_user_filter;     ///< Текущий фильтр по пользователям
};

#endif