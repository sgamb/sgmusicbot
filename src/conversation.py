# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    conversation.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: sgambari <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 15:21:06 by sgambari          #+#    #+#              #
#    Updated: 2023/04/12 18:19:05 by sgambari         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from telegram import (
        InlineKeyboardButton,
        InlineKeyboardMarkup,
        Update,
)
from telegram.ext import (
        CallbackQueryHandler,
        CommandHandler,
        ContextTypes,
        ConversationHandler,
)

from shelf import Record

async def years(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=year,
                    callback_data=year,
                )
            ]
            for year in range(3)
        ]
    )
    await update.message.reply_text(
            text="Years",
            reply_markup=keyboard,
    )
    return ALBUM


async def albums(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #TODO: can not recieve a query
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=album.record_name,
                    callback_data=album.id,
                )
            ]
            for album in range(update.callback_query.data)
        ]
    )
    await update.callback_query.edit_message_text(
            text=f"Albums of {update.callback_query.data}",
            reply_markup=keyboard,
    )
    return ConversationHandler.END


ALBUM = 0
years_handler = ConversationHandler(
    entry_points=[CommandHandler("years", years)],
    states={
        ALBUM: [CallbackQueryHandler(albums)],
    },
    fallbacks=[],
)
