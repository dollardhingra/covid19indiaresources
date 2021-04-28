import os
import logging
from typing import Tuple

import config
from twitter_url_generator import TwitterUrlGenerator
from custom_logger import CustomLogger as logger_
import telegram
from telegram import Update, ReplyKeyboardMarkup, ParseMode
from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
    ConversationHandler,
    CallbackContext,
)

SELECT_CITY, SELECT_CITY_CUSTOM, SELECT_FILTERS = range(3)
PORT = int(os.environ.get('PORT', 8443))


def format_message_and_get_parse_mode(
    url: str, update: Update
) -> Tuple[str, ParseMode]:
    logging.info(
        f"{logger_.get_formatted_str(update)} Formatting the url: {url}"
    )
    parse_mode = telegram.ParseMode.HTML
    message = TwitterUrlGenerator.format_url_as_html(url)

    return message, parse_mode


def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    logging.info(f"{logger_.get_formatted_str(update)} new session started..")
    reply_keyboard = [
        [
            "Delhi",
            "Noida",
            "Gurugram",
        ],
        ["Enter the city name myself"],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Hi, I will help you in finding oxygen cylinders, hospital beds, "
        "icu & ventilator beds, food and medicines for covid19 on "
        "twitter. Please select the city you want to search for:\n "
        "To start again click /start\n",
        reply_markup=markup,
    )
    logging.info(
        f"{logger_.get_formatted_str(update)}  Waiting for user's input.."
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return SELECT_CITY


def add_city(update: Update, context: CallbackContext) -> int:
    """
    :param city:
    :param context:
    :return:
    """
    text = update.message.text
    context.user_data["city"] = text
    logging.info(f"{logger_.get_formatted_str(update)}  city {text} added ")

    reply_keyboard = [
        ["beds", "icu", "oxygen", "ventilator"],
        ["tests", "favipiravir", "fabiflu"],
        ["tocilizumab", "remdesivir"],
        ["plasma", "food"],
        ["All of these.."],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Select the filter you want to search for. If you want to search all "
        "then select: All of the above.\n To start again click /start",
        reply_markup=markup,
    )
    logging.info(
        f"{logger_.get_formatted_str(update)}  Waiting for user's input for "
        f"filter"
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return SELECT_FILTERS


def add_city_custom(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Enter the name of the city.. To start again click /start"
    )

    logging.info(
        f"{logger_.get_formatted_str(update)}  Waiting for user's input for "
        f"custom city"
    )
    return SELECT_CITY_CUSTOM


def add_filter(update: Update, context: CallbackContext) -> int:
    logging.info(
        f"{logger_.get_formatted_str(update)} inside the add_filter method.."
    )
    mapping_search = {
        "beds": "bed+OR+beds",
        "icu": "icu",
        "ventilator": "ventilator+OR+ventilators",
        "oxygen": "oxygen",
        "tests": "test+OR+tests+OR+testing",
        "fabiflu": "fabiflu",
        "remdesivir": "remdesivir",
        "favipiravir": "favipiravir",
        "tocilizumab": "tocilizumab",
        "plasma": "plasma",
        "food": "tiffin+OR+food",
    }

    text = update.message.text
    if text == "All of these..":
        url = TwitterUrlGenerator(context.user_data["city"]).generate_url()
        logging.info(
            f"{logger_.get_formatted_str(update)} url generated(All Case): "
            f"{url}"
        )
    else:
        logging.info(f"selected filter: {text}")
        query_string = mapping_search[text]
        logging.info(
            f"{logger_.get_formatted_str(update)} query_string for selected "
            f"filter: {query_string}"
        )

        url = TwitterUrlGenerator(context.user_data["city"]).generate_url(
            query_string=query_string
        )
        logging.info(
            f"{logger_.get_formatted_str(update)} url generated(specific case)"
            f": {url}"
        )

    message, parse_mode = format_message_and_get_parse_mode(url, update)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message, parse_mode=parse_mode
    )

    update.message.reply_text("To start again click /start")


def main() -> None:
    # Create the Updater and pass it your bot's token.
    logging.info("Creating updaters and dispatchers...")
    updater = Updater(config.TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    logging.info("Updater and Dispatcher created.")

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_CITY: [
                MessageHandler(
                    Filters.regex("^(Delhi|Noida|Gurugram)$"), add_city
                ),
                MessageHandler(
                    Filters.regex("^Enter the city name myself$"),
                    add_city_custom,
                ),
            ],
            SELECT_CITY_CUSTOM: [
                MessageHandler(
                    Filters.text
                    & ~(Filters.command | Filters.regex("^Noted")),
                    add_city,
                )
            ],
            SELECT_FILTERS: [
                MessageHandler(
                    Filters.regex(
                        "^(beds|oxygen|ventilator|remdesivir|favipiravir|"
                        "tocilizumab|plasma|food|tests|icu|fabiflu)$"
                    ),
                    add_filter,
                ),
                MessageHandler(Filters.regex("^All of these..$"), add_filter),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dispatcher.add_handler(conv_handler)
    logging.info("Handlers added to dispatcher.")

    # Start the Bot
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=config.TELEGRAM_TOKEN,
        webhook_url=f"https://covid19indiaresources.herokuapp.com/{config.TELEGRAM_TOKEN}"
    )

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
