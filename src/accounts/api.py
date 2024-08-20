from django.contrib import auth
from django.shortcuts import get_object_or_404
from mail_templated import send_mail
from ninja import Router
from ninja.errors import HttpError

from megazord.api.auth import BadCredentials, create_jwt
from megazord.api.codes import ERROR_CODES
from megazord.api.requests import APIRequest
from megazord.schemas import ErrorSchema, StatusSchema

from .models import Account, ConfirmationCode
from .schemas import (
    ActivationSchema,
    EmailSchema,
    LoginSchema,
    RegisterResponseSchema,
    RegisterSchema,
    TokenSchema,
)

router = Router()


@router.post(
    path="/signup",
    summary="Register user",
    response={201: RegisterResponseSchema, 409: ErrorSchema, 422: ErrorSchema},
)
def signup(
    request: APIRequest, schema: RegisterSchema
) -> tuple[int, RegisterResponseSchema]:
    if "," in schema.username:
        raise HttpError(422, "Username cannot contain commas.")

    account = Account.objects.create_user(
        email=schema.email,
        username=schema.username,
        password=schema.password,
        is_organizator=schema.is_organizator,
        age=schema.age,
        city=schema.city,
        work_experience=schema.work_experience,
    )
    confirmation_code = ConfirmationCode.generate(user=account)

    send_mail(
        template_name="accounts/account_confirmation.html",
        context={"code": confirmation_code.code},
        from_email="",
        recipient_list=[account.email],
    )

    return 201, account


@router.post(path="/activate", response={200: StatusSchema, ERROR_CODES: ErrorSchema})
def activate_account(
    request: APIRequest, activation_schema: ActivationSchema
) -> tuple[int, StatusSchema | ErrorSchema]:
    code = get_object_or_404(
        ConfirmationCode,
        user__email=activation_schema.email,
        code=activation_schema.code,
    )
    code.delete()
    if code.is_expired:
        return 400, ErrorSchema(detail="Code expired")

    code.user.is_active = True
    code.user.save()

    return 200, StatusSchema()


@router.post(
    path="/resend_code", response={200: StatusSchema, ERROR_CODES: ErrorSchema}
)
def resend_code(
    request: APIRequest, email_schema: EmailSchema
) -> tuple[int, StatusSchema | ErrorSchema]:
    user = get_object_or_404(Account, email=email_schema.email)
    confirmation_code = ConfirmationCode.objects.filter(user=user).first()
    if confirmation_code and not confirmation_code.is_expired:
        return 400, ErrorSchema(detail="Code has not expired yet")

    confirmation_code = ConfirmationCode.generate(user=user)

    send_mail(
        template_name="accounts/account_confirmation.html",
        context={"code": confirmation_code.code},
        from_email="",
        recipient_list=[user.email],
    )

    return 200, StatusSchema()


@router.post(
    path="/signin",
    summary="Login user",
    response={200: TokenSchema, 404: ErrorSchema, 422: ErrorSchema},
)
def signin(request: APIRequest, schema: LoginSchema) -> tuple[int, TokenSchema]:
    account = auth.authenticate(username=schema.email, password=schema.password)
    if account is None:
        raise BadCredentials()

    token = create_jwt(user_id=account.id)
    return 200, TokenSchema(token=token)
