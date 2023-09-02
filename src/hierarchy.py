# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    hierarchy.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: sgambari <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 15:21:06 by sgambari          #+#    #+#              #
#    Updated: 2023/09/02 05:47:15 by serge            ###   ########.fr        #
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
from utils import send_album


async def years(update: Update, context: ContextTypes.DEFAULT_TYPE):
    years = Record.years()
    keyboard = []
    for i in range( len(years) // 2):
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=years[i][2:],  #TODO: starting from zero
                    callback_data=years[i],
                ),
                InlineKeyboardButton(
                    text=years[i + (len(years) // 2)][2:],  #TODO: up to heavean
                    callback_data=years[i + (len(years) // 2)],
                ),
            ]
        )
    await update.callback_query.edit_message_text(
            text="Imagine, that you are in an elevator. Now, pick your floor...",
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
            text=f"Some albums from 19{update.callback_query.data[2:]}...",
            reply_markup=keyboard,
    )
    #  TODO: ADD GO BACK BUTTTTTTTTTTON
    return TRACKS


async def tracks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    album_id = update.callback_query.data
    await update.callback_query.edit_message_text(
            text="Sending <ALBUM {album_id} TITLE>",  #TODO: get album title
    )
    await send_album(album_id, update)
    return ConversationHandler.END


ALBUMS, TRACKS = range(2)
years_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(years, pattern="Years")],
    states={
        ALBUMS: [CallbackQueryHandler(albums, pattern="y_")],
        TRACKS: [CallbackQueryHandler(tracks)],
    },
    fallbacks=[],
    per_message=True,
)

years_entry_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Years",
                    callback_data="Years",
                )
            ]
        ]
)
