-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Getting a list of the tables in the db
.tables

-- getting the schema for the tables so I can have an overview of how they connect and what information they have
.schema

-- gathering information about the theft on  July 28, 2023 on Humphrey Street.
SELECT description
FROM crime_scene_reports
WHERE month = 7
AND day = 28
AND year = 2023
AND street = 'Humphrey Street';

-- the above returned:
-- | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time –
-- each of their interview transcripts mentions the bakery. |
-- | Littering took place at 16:36. No known witnesses.
-- Looking into witnesses at the Humphrey Street bakery on July 28, 2023
SELECT transcript
FROM interviews
WHERE year = 2023
AND month = 7
AND day = 28
AND transcript LIKE '%bakery%';

-- Returned:
-- | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery
-- parking lot and drive away. If you have security footage from the bakery parking lot,
-- you might want to look for cars that left the parking lot in that time frame.                                                          |
-- | I don't know the thief's name, but it was someone I recognized.
-- Earlier this morning, before I arrived at Emma's bakery,
-- I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
-- | As the thief was leaving the bakery, they called someone who talked to
-- them for less than a minute. In the call, I heard the thief say that they were
-- planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket. |

-- Theft happened at 10:15 am, between 10:15 and 10:25, the thief got into a car at the bakery
-- Sometime between 10:15 am and 10:25 am, the theif called someone to
-- purchase a flight ticket, earliest time the next day
-- Call lasted less than 1 minute
-- Thief was withdrawing money from the ATM on Leggett street before 10:15 am

-- Looking into call logs between 10:15 and 10:25am, ordering by caller to make it easier to find duplicates
SELECT caller, receiver, duration
FROM phone_calls
WHERE year = 2023
AND month = 7
AND day = 28
AND duration < 60
ORDER BY caller;

-- Results:
-- +----------------+----------------+----------+
-- |     caller     |    receiver    | duration |
-- +----------------+----------------+----------+
-- | (031) 555-6622 | (910) 555-3251 | 38       |
-- | (130) 555-0289 | (996) 555-8899 | 51       |
-- | (286) 555-6063 | (676) 555-6554 | 43       |
-- | (338) 555-6650 | (704) 555-2131 | 54       |
-- | (367) 555-5533 | (375) 555-8161 | 45       |
-- | (499) 555-9472 | (892) 555-8872 | 36       |
-- | (499) 555-9472 | (717) 555-1342 | 50       |
-- | (770) 555-1861 | (725) 555-3243 | 49       |
-- | (826) 555-1652 | (066) 555-9701 | 55       |
-- +----------------+----------------+----------+

-- Checking the ATM usage before 10:15am on Legget Street
SELECT name, passport_number, license_plate, phone_number, atm_location
FROM people
    JOIN bank_accounts
    ON people.id = bank_accounts.person_id
        JOIN atm_transactions
        ON bank_accounts.account_number = atm_transactions.account_number
            WHERE atm_transactions.year = 2023
            AND atm_transactions.month = 7
            AND atm_transactions.day = 28
            AND atm_location = 'Leggett Street';
-- Results:
-- +---------+-----------------+---------------+----------------+----------------+
-- |  name   | passport_number | license_plate |  phone_number  |  atm_location  |
-- +---------+-----------------+---------------+----------------+----------------+
-- | Bruce   | 5773159633      | 94KL13X       | (367) 555-5533 | Leggett Street |
-- | Kaelyn  | 8304650265      | I449449       | (098) 555-1164 | Leggett Street |
-- | Diana   | 3592750733      | 322W7JE       | (770) 555-1861 | Leggett Street |
-- | Brooke  | 4408372428      | QX4YZN3       | (122) 555-4581 | Leggett Street |
-- | Kenny   | 9878712108      | 30G67EN       | (826) 555-1652 | Leggett Street |
-- | Iman    | 7049073643      | L93JTIZ       | (829) 555-5269 | Leggett Street |
-- | Luca    | 8496433585      | 4328GD8       | (389) 555-5198 | Leggett Street |
-- | Taylor  | 1988161715      | 1106N58       | (286) 555-6063 | Leggett Street |
-- | Benista | 9586786673      | 8X428L0       | (338) 555-6650 | Leggett Street |
-- +---------+-----------------+---------------+----------------+----------------+

-- Next step is to match the phone numbers with the callers from those times

SELECT name, passport_number, license_plate, phone_number, atm_location
FROM people
    JOIN bank_accounts
    ON people.id = bank_accounts.person_id
        JOIN atm_transactions
        ON bank_accounts.account_number = atm_transactions.account_number
            JOIN phone_calls
            ON people.phone_number = phone_calls.caller
                WHERE atm_transactions.year = 2023
                AND atm_transactions.month = 7
                AND atm_transactions.day = 28
                AND atm_location = 'Leggett Street'
                AND phone_calls.year = 2023
                AND phone_calls.month = 7
                AND phone_calls.day = 28
                AND phone_calls.duration < 60;

-- Results:
-- |  name   | passport_number | license_plate |  phone_number  |  atm_location  |
-- +---------+-----------------+---------------+----------------+----------------+
-- | Bruce   | 5773159633      | 94KL13X       | (367) 555-5533 | Leggett Street |
-- | Diana   | 3592750733      | 322W7JE       | (770) 555-1861 | Leggett Street |
-- | Kenny   | 9878712108      | 30G67EN       | (826) 555-1652 | Leggett Street |
-- | Taylor  | 1988161715      | 1106N58       | (286) 555-6063 | Leggett Street |
-- | Benista | 9586786673      | 8X428L0       | (338) 555-6650 | Leggett Street |
-- +---------+-----------------+---------------+----------------+----------------+

-- Checking the security logs for license plates of cars in the parking lot on July 28, 2023 between 10:15 and 10:25:
SELECT license_plate, activity
FROM bakery_security_logs
WHERE year = 2023
AND month = 7
AND day = 28
AND hour = 10
AND minute > 14 AND minute < 26;

-- Filtering to just show the cars exiting:
SELECT license_plate, activity
FROM bakery_security_logs
WHERE activity = 'exit'
AND year = 2023
AND month = 7
AND day = 28
AND hour = 10
AND minute > 14
AND minute < 26;
--Results:
-- +---------------+----------+
-- | license_plate | activity |
-- +---------------+----------+
-- | 5P2BI95       | exit     |
-- | 94KL13X       | exit     |
-- | 6P58WS2       | exit     |
-- | 4328GD8       | exit     |
-- | G412CB7       | exit     |
-- | L93JTIZ       | exit     |
-- | 322W7JE       | exit     |
-- | 0NTHK55       | exit     |
-- +---------------+----------+

-- From an earlier search, bruce and diana both had cars exit the bakery at that time:
-- |  name   | passport_number | license_plate |  phone_number  |  atm_location  |
-- +---------+-----------------+---------------+----------------+----------------+
-- | Bruce   | 5773159633      | 94KL13X       | (367) 555-5533 | Leggett Street |
-- | Diana   | 3592750733      | 322W7JE       | (770) 555-1861 | Leggett Street |
-- Both Bruce and Diana made a call lasting less than 60 seconds that day

-- Checking flights leaving fiftyville early on the 29th (next day) and matches bruce or diana's passport
SELECT passport_number, flights.hour, flights.minute, flights.destination_airport_id
FROM passengers
    JOIN flights
    ON passengers.flight_id = flights.id
        JOIN airports
        ON flights.origin_airport_id = airports.id
        WHERE airports.city
        LIKE 'Fiftyville'
        AND year = 2023
        AND month = 7
        AND day = 29
        AND (passengers.passport_number = 5773159633 OR passengers.passport_number = 3592750733)
        ORDER BY flights.hour, flights.minute;

-- Results:
-- +-----------------+------+--------+------------------------+
-- | passport_number | hour | minute | destination_airport_id |
-- +-----------------+------+--------+------------------------+
-- | 5773159633      | 8    | 20     | 4                      |
-- | 3592750733      | 16   | 0      | 6                      |
-- +-----------------+------+--------+------------------------+

-- Passport 5773159633 matches with Bruce, phone number: (367) 555-5533
-- Bruce flew into airport id 4. Locating which city Bruce flew into:
SELECT full_name, city
FROM airports
WHERE id = 4;

-- Results:
-- +-------------------+---------------+
-- |     full_name     |     city      |
-- +-------------------+---------------+
-- | LaGuardia Airport | New York City |
-- +-------------------+---------------+

-- Discovering Bruce's accomplice's phone number based on his phone number and the call on July 28th, 2023:
SELECT phone_calls.receiver
FROM phone_calls
WHERE phone_calls.year = 2023
AND phone_calls.month = 7
AND phone_calls.day = 28
AND phone_calls.duration < 60
AND phone_calls.caller = '(367) 555-5533';

-- Results:
-- +----------------+
-- |    receiver    |
-- +----------------+
-- | (375) 555-8161 |
-- +----------------+

-- Finding who owns the phone number that Bruce called:
SELECT name
FROM people
WHERE phone_number = '(375) 555-8161';

-- Results:
-- +-------+
-- | name  |
-- +-------+
-- | Robin |
-- +-------+
