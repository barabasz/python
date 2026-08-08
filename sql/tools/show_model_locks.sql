-- =============================================================================
-- tools.show_model_locks
-- =============================================================================
-- Pokazuje sesje trzymające locki na bazie model i generuje polecenia KILL.
--
-- Wymagania:
--   - Schemat "tools" musi istnieć (CREATE SCHEMA tools;).
--   - Uprawnienia do widokow DMV: sys.dm_tran_locks, sys.dm_exec_sessions.
--
-- Użycie:
--   EXEC tools.show_model_locks;
--
-- Wynik:
--   1) Lista sesji z lockami na model
--      (session_id, login_name, host_name, program_name, status, resource_type,
--       request_mode, request_status)
--   2) Zestaw poleceń KILL do skopiowania i wykonania.
-- =============================================================================

CREATE OR ALTER PROCEDURE tools.show_model_locks
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @model_db_id int = DB_ID('model');

    -- Tabela tymczasowa z sesjami trzymającymi locki na model
    SELECT
        l.request_session_id AS session_id,
        s.login_name,
        s.host_name,
        s.program_name,
        s.status,
        l.resource_type,
        l.request_mode,
        l.request_status
    INTO #model_locks
    FROM sys.dm_tran_locks AS l
    JOIN sys.dm_exec_sessions AS s
        ON l.request_session_id = s.session_id
    WHERE l.resource_database_id = @model_db_id;

    IF EXISTS (SELECT 1 FROM #model_locks)
    BEGIN
        -- 1) Informacja o sesjach
        SELECT 'Sesje trzymające locki na bazie model:' AS [Info];

        SELECT
            session_id,
            login_name,
            host_name,
            program_name,
            status,
            resource_type,
            request_mode,
            request_status
        FROM #model_locks
        ORDER BY session_id;

        -- 2) Generowanie poleceń KILL
        SELECT 'Polecenia KILL do wykonania:' AS [Info];

        SELECT
            'KILL ' + CONVERT(varchar(10), session_id) + ';' AS kill_command
        FROM #model_locks
        ORDER BY session_id;
    END
    ELSE
    BEGIN
        -- Brak blokad na model
        SELECT 'Brak sesji trzymających locki na bazie model.' AS [Info];
    END;

    DROP TABLE #model_locks;
END;
GO

-- Przyklad uzycia:
-- EXEC tools.show_model_locks;
