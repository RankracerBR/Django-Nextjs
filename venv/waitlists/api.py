from django.shortcuts import get_object_or_404
from ninja import Router
from typing import List

import helpers
from ninja_jwt.authentication import JWTAuth

from .schemas import (WaitlistEntryListSchema,
                      WaitlistEntryDetailSchema,
                      WaitlistEntryCreateSchema)
from .models import WaitlistEntry


router = Router()


# /api/waitlists/
@router.get("", response=List[WaitlistEntryListSchema], auth=helpers.api_auth_user_required)
def list_waitlist_entries(request):
    qs = WaitlistEntry.objects.all(user=request.user)
    return qs

#/api/waitlists/
@router.post("", response=WaitlistEntryDetailSchema, 
auth=helpers.api_auth_user_or_annon)
def create_waitlist_entry(request, data: WaitlistEntryCreateSchema):
    obj = WaitlistEntry(**data.dict())
    print(request.user)
    if request.user.is_authenticated:
        obj.user = request.user
        # obj.user_id = request.user.id
    obj.save()
    return obj

@router.get("{entry_id}/", response=WaitlistEntryDetailSchema,
             auth=helpers.api_auth_user_required)
def get_waitlist_entries(request, entry_id: int):
    obj = get_object_or_404(
        WaitlistEntry, 
        id=entry_id,
        user=request.user)
    return obj