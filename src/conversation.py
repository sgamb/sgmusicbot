# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    conversation.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: sgambari <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 15:21:06 by sgambari          #+#    #+#              #
#    Updated: 2023/04/29 13:23:22 by sgambari         ###   ########.fr        #
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
from main import send_album


async def years(update: Update, context: ContextTypes.DEFAULT_TYPE):
    years = Record.years()
    keyboard = []
    for i in range(0, len(years), 2):
        if i == (len(years) - 1):
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=years[i],
                        callback_data=years[i],
                    ),
                ]
            )
        else:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=years[i],
                        callback_data=years[i],
                    ),
                    InlineKeyboardButton(
                        text=years[i + 1],
                        callback_data=years[i + 1],
                    ),
                ]
            )
    await update.message.reply_text(
            text="Years",
            reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ALBUMS


async def albums(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=album.record_name,
                    callback_data=album.id,
                )
            ]
            for album in Record.by_year(update.callback_query.data)
        ]
    )
    await update.callback_query.edit_message_text(
            text=f"Albums of {update.callback_query.data}",
            reply_markup=keyboard,
    )
    return TRACKS


async def tracks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    album_id = update.callback_query.data
    await send_album(album_id, update)
    return ConversationHandler.END


ALBUMS, TRACKS = range(2)
years_handler = ConversationHandler(
    entry_points=[CommandHandler("years", years)],
    states={
        ALBUMS: [CallbackQueryHandler(albums)],
        TRACKS: [CallbackQueryHandler(tracks)],
    },
    fallbacks=[],
)
