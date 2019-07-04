from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CallbackContext, InlineQueryHandler, Dispatcher


class InlineHandler:
    def get_handler(self):
        return InlineQueryHandler(self.handle)

    def handle(self, update: Update, context: CallbackContext):
        query = update.inline_query.query
        if not query:
            return
        results = list()
        results.append(
            InlineQueryResultArticle(
                id=query.upper(),
                title='Caps',
                input_message_content=InputTextMessageContent(query.upper())
            )
        )
        context.bot.answer_inline_query(update.inline_query.id, results)


def init(dispatcher: Dispatcher):
    dispatcher.add_handler(InlineHandler().get_handler())
