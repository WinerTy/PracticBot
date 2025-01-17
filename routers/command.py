from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command


from database import db_helper
from database.crud import UserRepository
from database.schemas import PhoneNumber, FullName
from utils import UserRegistration
from logger import logger

command_router = Router()


@command_router.message(Command("start"))
async def start(message):
    logger.info(f"Пользователь {message.from_user.id} вызвал команду /start")
    await message.answer("Привет! Я бот для регистрации пользователей.")


@command_router.message(Command("help"))
async def help_message(message):
    logger.info(f"Пользователь {message.from_user.id} вызвал команду /help")
    await message.answer("Help")


@command_router.message(Command("register"))
async def register(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} начал регистрацию")
    await message.answer("Регистрация")
    await state.set_state(UserRegistration.phone)
    await message.answer("Введите номер телефона")


@command_router.message(UserRegistration.phone)
async def process_phone(message: types.Message, state: FSMContext):
    phone_number = message.text
    logger.info(
        f"Пользователь {message.from_user.id} ввел номер телефона: {phone_number}"
    )

    try:
        phone_data = PhoneNumber(phone=phone_number)
        validated_phone = phone_data.phone

        async for session in db_helper.session_getter():
            user_repo = UserRepository(session)
            user = await user_repo.get_user_by_phone(validated_phone)

            if user:
                logger.warning(
                    f"Пользователь с номером {validated_phone} уже зарегистрирован"
                )
                await message.answer(
                    "Пользователь с таким номером уже зарегистрирован."
                )
                await state.clear()
            else:
                logger.info(
                    f"Номер телефона {validated_phone} валиден, запрашиваем имя"
                )
                await state.update_data(phone=validated_phone)
                await message.answer(
                    "Введите имя и фамилию, чтобы завершить регистрацию."
                )
                await state.set_state(UserRegistration.full_name)

    except ValueError as e:
        logger.error(f"Ошибка валидации номера телефона: {str(e)}")
        await message.answer("Некорректный номер телефона.")
        await state.clear()


@command_router.message(UserRegistration.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    logger.info(f"Пользователь {message.from_user.id} ввел имя: {full_name}")

    data = await state.get_data()
    phone_number = data.get("phone")

    try:
        full_name_data = FullName(full_name=full_name)
        validated_full_name = full_name_data.full_name
        async for session in db_helper.session_getter():
            user_repo = UserRepository(session)
            await user_repo.create_user(
                phone_number, validated_full_name, message.from_user.id
            )
            await message.answer(f"Пользователь {validated_full_name} зарегистрирован.")
            logger.info(f"Пользователь {validated_full_name} успешно зарегистрирован")
    except ValueError:
        await message.answer("Некорректное имя и фамилия.")

    finally:
        await state.clear()


@command_router.message(Command("list"))
async def list_users(message: types.Message):
    async for session in db_helper.session_getter():
        user_repo = UserRepository(session)
        users = await user_repo.get_all_users()
        await message.answer(f"Список пользователей:\n{users}")
