# S3 + JWT + deployment guidance

This branch adds support for the following production features:

1) S3-backed media storage (django-storages + boto3)
   - Set these environment variables in your Railway (or host):
     AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME
   - When those are present, the Django settings will configure DEFAULT_FILE_STORAGE to use S3. Generated exit-pass PDFs will be stored in S3.

2) JWT authentication (Simple JWT)
   - The API now uses DRF + Simple JWT as its default auth. Endpoints require authentication except the parent registration and token obtain endpoints.
   - Obtain tokens via POST /api/token/ with {username, password}. Refresh via /api/token/refresh/
   - The Next.js frontend should store the access token (e.g., HTTP-only cookie or memory) and send Authorization: Bearer <token> for protected API calls.

3) API permission behavior
   - Parents: can create accounts (parents/register) and, once authenticated, can list/create students tied to their account and create permission requests for their students.
   - Staff: depending on role (Profile), may view/process requests via the admin or the website UI. You may want to add role-based decorators for staff-only views.

4) How to test locally
   - If you don't set AWS_* env vars, the app will use local MEDIA_ROOT for files.
   - To test JWT flows locally:
     - Create a parent via POST /api/parents/register/ (or use the frontend)
     - Obtain token: POST /api/token/ {username, password}
     - Use Authorization header to call protected endpoints.

If you want, I can also:
- Update the Next.js frontend to obtain/store JWTs and authenticate requests automatically (login page + token storage). Do you want me to add that frontend work too?