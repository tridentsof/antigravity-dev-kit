---
name: aspnet-patterns
description: ASP.NET Core patterns - Controllers, Services, Middleware
---

# ASP.NET Core Patterns

> Clean architecture for ASP.NET Core applications.

---

## Architecture

```
Controller → Service → Repository → Database
```

| Layer | Responsibility |
|-------|----------------|
| Controller | HTTP handling, validation |
| Service | Business logic |
| Repository | Data access |

---

## Controller Pattern

```csharp
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;

    public UsersController(IUserService userService)
    {
        _userService = userService;
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<UserDto>> GetById(int id)
    {
        var user = await _userService.GetByIdAsync(id);
        return user is null ? NotFound() : Ok(user);
    }

    [HttpPost]
    public async Task<ActionResult<UserDto>> Create(CreateUserDto dto)
    {
        var user = await _userService.CreateAsync(dto);
        return CreatedAtAction(nameof(GetById), new { id = user.Id }, user);
    }
}
```

---

## Service Pattern

```csharp
public class UserService : IUserService
{
    private readonly IUserRepository _repository;

    public UserService(IUserRepository repository)
    {
        _repository = repository;
    }

    public async Task<UserDto?> GetByIdAsync(int id)
    {
        var user = await _repository.GetByIdAsync(id);
        return user?.ToDto();
    }
}
```

---

## Dependency Injection

```csharp
// Program.cs
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<IUserRepository, UserRepository>();
```

---

## Response Format

```csharp
public class ApiResponse<T>
{
    public bool Success { get; set; }
    public T? Data { get; set; }
    public string? Error { get; set; }
}
```

---

## HTTP Status Codes

| Method | Success | Error |
|--------|---------|-------|
| GET | 200 OK | 404 Not Found |
| POST | 201 Created | 400 Bad Request |
| PUT | 200 OK | 404 Not Found |
| DELETE | 204 No Content | 404 Not Found |

---

## DO / DON'T

| ✅ Do | ❌ Don't |
|-------|---------|
| Async/await | Blocking calls |
| DI everywhere | `new` in controllers |
| Proper status codes | 200 for everything |
| Constants/Enums for strings | Magic strings |
| Environment variables/Config | Hardcoded settings |
