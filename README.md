### Backend Validation and Error Handling Testing

#### 1. Server-side Form Validation
- [ ] Submit forms with missing required fields.
- [ ] Submit invalid time ranges.
- [ ] Submit invalid building or room selections.
- [ ] Submit multiple entries with at least one invalid entry.
- [ ] Verify invalid data is not saved to the database.

#### 2. Business Rule Validation
- [ ] Test overlapping schedules on the same day.
- [ ] Test schedules that overlap at the beginning and end.
- [ ] Test the same time slot on different days.
- [ ] Test invalid building-room relationships.
- [ ] Verify valid schedules are saved and invalid schedules are rejected.

#### 3. Success and Error Messages
- [ ] Verify success messages after successful actions.
- [ ] Verify error messages after failed validation.
- [ ] Verify conflict messages are understandable.
- [ ] Verify messages do not expose technical details.

#### 4. Custom Error Pages
- [ ] Test a nonexistent URL with DEBUG=False.
- [ ] Verify the custom 404 page is displayed.
- [ ] Trigger a test server error with DEBUG=False.
- [ ] Verify the custom 500 page is displayed.
- [ ] Remove temporary test routes and restore DEBUG=True.

#### 5. Invalid URLs and IDs
- [ ] Test nonexistent record IDs.
- [ ] Verify invalid IDs return a 404 response.
- [ ] Verify the application does not crash.
- [ ] Verify users cannot access other users' records by changing IDs.
- [ ] Implement and test get_object_or_404 in detail/edit/delete views.